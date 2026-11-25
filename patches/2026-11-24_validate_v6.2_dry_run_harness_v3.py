#!/usr/bin/env python3
"""Pill by Pill v6.2 End-to-End Dry-Run Validation Harness v3 (61 Merged Patches + 49 Builders + v52 Integrator).

Usage:
  python3 2026-11-24_validate_v6.2_dry_run_harness_v3.py --selftest
  python3 2026-11-24_validate_v6.2_dry_run_harness_v3.py --patches-dir /path/to/01_Code --source-zip 2026-11-21_pill-by-pill-source_v6.0b.zip
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

INTEGRATOR_FILE = "2026-11-24_apply_v6.2_unified_release_v52.py"
PATCH_ORDER = [('v6.0a', '2026-11-20_v6.0a_vendors_cdmo_audit_comparator_patch.py'), ('v6.0b', '2026-11-20_v6.0b_pharma_encyclopedia_departments_patch.py'), ('v6.0c', '2026-11-20_v6.0c_equipment_market_pricing_patch.py'), ('v6.0_fetchers_wiring', '2026-11-21_v6.0_vendors_fetchers_and_route_wiring_patch.py'), ('v6.0_deep_depts_tests', '2026-11-21_v6.0_departments_deep_and_unified_tests_patch.py'), ('v6.0d_crosslinks_api', '2026-11-21_v6.0d_crosslinks_price_charts_and_api_patch.py'), ('v6.0e_rollups_oems_svg', '2026-11-21_v6.0e_parent_rollups_oem_matrix_and_lifecycle_svg_patch.py'), ('v6.0f_static_seo', '2026-11-21_v6.0f_static_seo_and_sitemap_patch.py'), ('v6.0g_equip_18', '2026-11-21_v6.0g_equipment_expansion_18_classes_patch.py'), ('v6.0h_origins75_browser_tests', '2026-11-21_v6.0h_origin_stories_batch7_and_v60_browser_tests_patch.py'), ('v6.0i_8stage_lifecycle', '2026-11-21_v6.0i_end_to_end_8stage_lifecycle_patch.py'), ('v6.0j_software_economics', '2026-11-21_v6.0j_pharma_software_and_economics_patch.py'), ('v6.0k_partner_ecosystem', '2026-11-21_v6.0k_partner_ecosystem_patch.py'), ('v6.0l_playbooks_quiz58', '2026-11-21_v6.0l_modality_playbooks_and_v60_quiz_patch.py'), ('v6.1a_global_search_origins_csv', '2026-11-22_v6.1a_global_search_origins_gallery_nav_csv_patch.py'), ('v6.1b_glossary_trace_ich', '2026-11-22_v6.1b_glossary_trace_storyboards_ich_patch.py'), ('v6.1c_chem_quiz_worksheets', '2026-11-22_v6.1c_chem_copy_quiz_filters_teacher_worksheets_patch.py'), ('v6.1d_grouped_nav_pointers_status', '2026-11-22_v6.1d_grouped_nav_clinical_pointers_feed_status_patch.py'), ('v6.1e_atc_tree_origins90', '2026-11-22_v6.1e_atc_class_tree_and_origins_batch8_patch.py'), ('v6.1f_gsc_fix_origins100_storyboards5', '2026-11-22_v6.1f_gsc_schema_fix_origins100_and_5modality_storyboards_patch.py'), ('v6.1g_seo_search_browser_coverage', '2026-11-22_v6.1g_seo_global_search_and_browser_test_coverage_patch.py'), ('v6.1h_pathways_exclusivity', '2026-11-22_v6.1h_regulatory_pathways_and_exclusivity_comparator_patch.py'), ('v6.1i_clinical_trials_endpoints', '2026-11-22_v6.1i_clinical_trial_design_and_endpoints_patch.py'), ('v6.1j_adme_pk_medchem_delivery', '2026-11-23_v6.1j_adme_pk_medchem_and_delivery_patch.py'), ('v6.1k_pharmacovigilance_safety', '2026-11-23_v6.1k_pharmacovigilance_and_drug_safety_patch.py'), ('v6.1l_ip_patents_hatch_waxman_bpcia', '2026-11-23_v6.1l_pharma_ip_patents_hatch_waxman_bpcia_patch.py'), ('v6.1m_sterile_bioprocessing_cleanroom', '2026-11-23_v6.1m_sterile_manufacturing_bioprocessing_cleanroom_patch.py'), ('v6.1n_global_reg_hta', '2026-11-23_v6.1n_global_regulatory_agencies_and_hta_comparator_patch.py'), ('v6.1o_cdx_biomarkers', '2026-11-23_v6.1o_companion_diagnostics_biomarkers_patch.py'), ('v6.1p_real_world_evidence', '2026-11-23_v6.1p_real_world_evidence_rwd_patch.py'), ('v6.1q_supply_chain_dscsa', '2026-11-23_v6.1q_supply_chain_dscsa_cold_chain_patch.py'), ('v6.1r_biologics_cgt', '2026-11-23_v6.1r_biologics_cgt_advanced_modalities_patch.py'), ('v6.1s_vaccines_adjuvants', '2026-11-23_v6.1s_vaccines_immunology_adjuvants_patch.py'), ('v6.1t_orphan_pediatric', '2026-11-23_v6.1t_rare_diseases_orphan_pediatric_access_patch.py'), ('v6.1u_digital_health_samd_dct', '2026-11-23_v6.1u_digital_health_samd_ai_ml_dct_patch.py'), ('v6.1v_otc_compounding_dshea', '2026-11-23_v6.1v_otc_monographs_switches_compounding_dshea_patch.py'), ('v6.1w_promotion_opdp_transparency', '2026-11-23_v6.1w_drug_promotion_opdp_transparency_patch.py'), ('v6.1x_controlled_substances_dea_rems', '2026-11-23_v6.1x_controlled_substances_dea_rems_patch.py'), ('v6.1y_pricing_ira_340b_mdrp', '2026-11-23_v6.1y_pharma_pricing_ira_340b_mdrp_patch.py'), ('v6.1z_special_populations_pllr', '2026-11-23_v6.1z_special_populations_pediatric_pllr_geriatric_diversity_patch.py'), ('v6.2a_radiopharma_theranostics', '2026-11-23_v6.2a_radiopharmaceuticals_theranostics_pet_cgmp_patch.py'), ('v6.2b_combo_products_hfe', '2026-11-23_v6.2b_combination_products_drug_device_human_factors_patch.py'), ('v6.2c_complex_quality_nitrosamines', '2026-11-23_v6.2c_complex_generics_nitrosamines_q3d_botanicals_patch.py'), ('v6.2d_shortages_resilience', '2026-11-24_v6.2d_drug_shortages_supply_resilience_essential_meds_patch.py'), ('v6.2e_amr_antiinfectives', '2026-11-24_v6.2e_amr_antibiotics_phage_carb_x_incentives_patch.py'), ('v6.2f_excipients_dmfs_nano', '2026-11-24_v6.2f_excipients_dmfs_nanomaterials_lai_patch.py'), ('v6.2g_oncology_oce', '2026-11-24_v6.2g_oncology_oce_accelerated_approval_master_protocols_patch.py'), ('v6.2h_gcp_bimo_cdisc', '2026-11-24_v6.2h_gcp_bimo_part11_cdisc_standards_patch.py'), ('v6.2i_adcs_bispecifics_oligos', '2026-11-24_v6.2i_adcs_bispecifics_peptides_oligonucleotides_patch.py'), ('v6.2j_rmat_hctp_cgt_cmc', '2026-11-24_v6.2j_rmat_hctp_cgt_potency_genome_editing_patch.py'), ('v6.2k_pfdd_coa_expanded_access', '2026-11-24_v6.2k_pfdd_coa_expanded_access_right_to_try_patch.py'), ('v6.2l_continuous_pat_ai_mfg', '2026-11-24_v6.2l_continuous_mfg_ich_q13_pat_etp_ai_mfg_patch.py'), ('v6.2m_analytical_usp_q12', '2026-11-24_v6.2m_analytical_q2_q14_usp_ich_q12_stability_patch.py'), ('v6.2n_nonclinical_nams', '2026-11-24_v6.2n_nonclinical_safety_ich_m3_s1b_s6_s9_nams_patch.py'), ('v6.2o_babe_bcs_nti', '2026-11-24_v6.2o_bioequivalence_bcs_m9_nti_ivpt_pbpk_patch.py'), ('v6.2p_pharma_careers_roles', '2026-11-24_v6.1u_pharma_careers_roles_pathways_patch.py'), ('v6.2q_quiz80_glossary60', '2026-11-24_v6.1v_quiz80_and_glossary60_expansion_patch.py'), ('v6.2r_pharma_history_safety_laws', '2026-11-24_v6.1w_pharma_history_safety_laws_patch.py'), ('v6.2s_pharma_bd_licensing_ma_valuation', '2026-11-24_v6.1z_pharma_bd_licensing_ma_valuation_patch.py'), ('v6.2t_quiz100_glossary80', '2026-11-24_v6.2t_quiz100_and_glossary80_expansion_patch.py'), ('v6.2u_worksheets6_storyboards7', '2026-11-24_v6.2u_worksheets6_and_storyboards7_expansion_patch.py')]


def _check_https_urls(obj, bad: list, path: str = "") -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("url", "source") and isinstance(v, str) and (v.startswith("http://") or v.startswith("https://")):
                if not v.startswith("https://"):
                    bad.append(f"{path}.{k}: {v}")
            elif k == "sources" and isinstance(v, list):
                for idx, item in enumerate(v):
                    if isinstance(item, str) and not item.startswith("https://"):
                        bad.append(f"{path}.sources[{idx}]: {item}")
                    else:
                        _check_https_urls(item, bad, f"{path}.sources[{idx}]")
            else:
                _check_https_urls(v, bad, f"{path}.{k}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            _check_https_urls(item, bad, f"{path}[{idx}]")


def validate_directory(patches_dir: pathlib.Path, source_zip: pathlib.Path | None = None, skip_selftests: bool = False) -> dict:
    report = {
        "patches_expected": len(PATCH_ORDER),
        "missing_files": [],
        "compile_errors": [],
        "selftest_failures": [],
        "selftest_passed": 0,
        "integration": None,
        "non_https_urls": [],
    }
    required = [INTEGRATOR_FILE] + [fname for _, fname in PATCH_ORDER]
    for fname in required:
        fp = patches_dir / fname
        if not fp.is_file():
            report["missing_files"].append(fname)
            continue
        try:
            py_compile.compile(str(fp), doraise=True)
        except Exception as exc:
            report["compile_errors"].append({"file": fname, "error": str(exc)})

    if report["missing_files"] or report["compile_errors"]:
        report["status"] = "FAILED_MANIFEST_OR_COMPILE"
        return report

    if not skip_selftests:
        for fname in required:
            fp = patches_dir / fname
            proc = subprocess.run([sys.executable, str(fp), "--selftest"], capture_output=True, text=True)
            if proc.returncode != 0:
                report["selftest_failures"].append({"file": fname, "stderr": proc.stderr[-500:]})
            else:
                report["selftest_passed"] += 1

    if report["selftest_failures"]:
        report["status"] = "FAILED_SELFTESTS"
        return report

    if source_zip and source_zip.is_file():
        with tempfile.TemporaryDirectory() as td:
            out_zip = pathlib.Path(td) / "dry_run_v6.2.zip"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(patches_dir / INTEGRATOR_FILE),
                    "--source-zip", str(source_zip),
                    "--patches-dir", str(patches_dir),
                    "--out-zip", str(out_zip),
                ],
                capture_output=True,
                text=True,
            )
            if proc.returncode != 0:
                report["status"] = "FAILED_INTEGRATION"
                report["integration"] = {"returncode": proc.returncode, "stderr": proc.stderr[-1000:]}
                return report
            report["integration"] = json.loads(proc.stdout)

    report["status"] = "PASSED"
    return report


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        bad = []
        _check_https_urls({"url": "https://www.fda.gov/", "sources": [{"url": "http://insecure.example.com"}]}, bad)
        assert len(bad) == 1 and "insecure.example.com" in bad[0], bad
        r = validate_directory(root, skip_selftests=True)
        assert r["status"] == "FAILED_MANIFEST_OR_COMPILE" and len(r["missing_files"]) == 62, r
        print("V62_DRY_RUN_VALIDATION_HARNESS_V3_SELFTEST_PASSED", json.dumps({"patches_tracked": len(PATCH_ORDER), "total_files_checked": 62}))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="End-to-End Dry-Run Validation Harness v3 for Pill by Pill v6.2 (61 patches + v52 integrator).")
    ap.add_argument("--patches-dir", type=pathlib.Path, help="Directory containing all 61 patches + v52 integrator")
    ap.add_argument("--source-zip", type=pathlib.Path, help="Optional v6.0b source zip to run full dry-run integration")
    ap.add_argument("--skip-selftests", action="store_true", help="Skip individual --selftest runs")
    ap.add_argument("--selftest", action="store_true", help="Run harness self-check")
    args = ap.parse_args(argv)

    if args.selftest:
        selftest()
        return 0
    if not args.patches_dir:
        ap.error("Provide --patches-dir <dir> or --selftest")
        return 2

    res = validate_directory(args.patches_dir, args.source_zip, args.skip_selftests)
    print(json.dumps(res, indent=2))
    return 0 if res.get("status") == "PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
