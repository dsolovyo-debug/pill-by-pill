#!/usr/bin/env python3
"""Pill by Pill v6.1 Unified Release Integrator & Cleaner (v57 — complete v6.0a–v6.0l + v6.1a–v6.1z + v6.2a–v6.2u).

Applies the complete 61-patch v6.0 + v6.1a–z + v6.2a–u stack in deterministic dependency order onto an unpacked
`2026-11-21_pill-by-pill-source_v6.0b.zip` (or v5.26+) directory, runs all 52 builders
(`build_departments.py`, `build_vendors.py`, `build_equipment_catalog.py`,
`build_software_and_economics.py`, `build_partners.py`, `build_playbooks.py`,
`build_origins_gallery.py`, `build_v61b_reference.py`, `build_worksheets.py`,
`build_atc_tree.py`, `build_pathways.py`, `build_trials.py`, `build_adme.py`,
`build_safety.py`, `build_ip_patents.py`, `build_sterile_mfg.py`, `build_global_reg_hta.py`,
`build_diagnostics.py`, `build_rwe.py`, `build_supply_chain.py`, `build_biologics_cgt.py`,
`build_vaccines.py`, `build_orphan.py`, `build_digital_health.py`, `build_otc_compounding.py`,
`build_promotion_transparency.py`, `build_controlled_substances.py`, `build_pricing_access.py`,
`build_special_populations.py`, `build_radiopharma.py`, `build_combo_products.py`,
`build_complex_quality.py`, `build_shortages_resilience.py`, `build_amr_antiinfectives.py`,
`build_excipients_dmfs_nano.py`, `build_oncology_oce.py`, `build_gcp_bimo_cdisc.py`,
`build_adcs_bispecifics_oligos.py`, `build_rmat_hctp_cgt_cmc.py`, `build_pfdd_coa_expanded_access.py`,
`build_continuous_pat_ai_mfg.py`, `build_analytical_usp_q12.py`, `build_nonclinical_nams.py`,
`build_babe_bcs_nti.py`, `build_midd_pharmacometrics.py`, `build_labeling_spl_rems.py`,
`build_inspections_483_recalls.py`, `build_discovery_sbdd_protacs.py`, `build_packaging_el_dscsa.py`,
`build_user_fees_prv.py`, `build_global_search.py`, and `build_v60_static_pages.py`),
executes `tests/test_v60.py`, bumps `app.py` and `site/version.json` to `6.1`, and packages a
clean, `__pycache__`-free `pill-by-pill-source_v6.1.zip`.

Required patch files in `--patches-dir`:
  1. 2026-11-20_v6.0a_vendors_cdmo_audit_comparator_patch.py
  2. 2026-11-20_v6.0b_pharma_encyclopedia_departments_patch.py (skipped if build_departments.py already exists)
  3. 2026-11-20_v6.0c_equipment_market_pricing_patch.py
  4. 2026-11-21_v6.0_vendors_fetchers_and_route_wiring_patch.py
  5. 2026-11-21_v6.0_departments_deep_and_unified_tests_patch.py
  6. 2026-11-21_v6.0d_crosslinks_price_charts_and_api_patch.py
  7. 2026-11-21_v6.0e_parent_rollups_oem_matrix_and_lifecycle_svg_patch.py
  8. 2026-11-21_v6.0f_static_seo_and_sitemap_patch.py
  9. 2026-11-21_v6.0g_equipment_expansion_18_classes_patch.py
 10. 2026-11-21_v6.0h_origin_stories_batch7_and_v60_browser_tests_patch.py
 11. 2026-11-21_v6.0i_end_to_end_8stage_lifecycle_patch.py
 12. 2026-11-21_v6.0j_pharma_software_and_economics_patch.py
 13. 2026-11-21_v6.0k_partner_ecosystem_patch.py
 14. 2026-11-21_v6.0l_modality_playbooks_and_v60_quiz_patch.py
 15. 2026-11-22_v6.1a_global_search_origins_gallery_nav_csv_patch.py
 16. 2026-11-22_v6.1b_glossary_trace_storyboards_ich_patch.py
 17. 2026-11-22_v6.1c_chem_copy_quiz_filters_teacher_worksheets_patch.py
 18. 2026-11-22_v6.1d_grouped_nav_clinical_pointers_feed_status_patch.py
 19. 2026-11-22_v6.1e_atc_class_tree_and_origins_batch8_patch.py
 20. 2026-11-22_v6.1f_gsc_schema_fix_origins100_and_5modality_storyboards_patch.py
 21. 2026-11-22_v6.1g_seo_global_search_and_browser_test_coverage_patch.py
 22. 2026-11-22_v6.1h_regulatory_pathways_and_exclusivity_comparator_patch.py
 23. 2026-11-22_v6.1i_clinical_trial_design_and_endpoints_patch.py
 24. 2026-11-23_v6.1j_adme_pk_medchem_and_delivery_patch.py
 25. 2026-11-23_v6.1k_pharmacovigilance_and_drug_safety_patch.py
 26. 2026-11-23_v6.1l_pharma_ip_patents_hatch_waxman_bpcia_patch.py
 27. 2026-11-23_v6.1m_sterile_manufacturing_bioprocessing_cleanroom_patch.py
 28. 2026-11-23_v6.1n_global_regulatory_agencies_and_hta_comparator_patch.py
 29. 2026-11-23_v6.1o_companion_diagnostics_biomarkers_patch.py
 30. 2026-11-23_v6.1p_real_world_evidence_rwd_patch.py
 31. 2026-11-23_v6.1q_supply_chain_dscsa_cold_chain_patch.py
 32. 2026-11-23_v6.1r_biologics_cgt_advanced_modalities_patch.py
 33. 2026-11-23_v6.1s_vaccines_immunology_adjuvants_patch.py
 34. 2026-11-23_v6.1t_rare_diseases_orphan_pediatric_access_patch.py
 35. 2026-11-23_v6.1u_digital_health_samd_ai_ml_dct_patch.py
 36. 2026-11-23_v6.1v_otc_monographs_switches_compounding_dshea_patch.py
 37. 2026-11-23_v6.1w_drug_promotion_opdp_transparency_patch.py
 38. 2026-11-23_v6.1x_controlled_substances_dea_rems_patch.py
 39. 2026-11-23_v6.1y_pharma_pricing_ira_340b_mdrp_patch.py
 40. 2026-11-23_v6.1z_special_populations_pediatric_pllr_geriatric_diversity_patch.py
 41. 2026-11-23_v6.2a_radiopharmaceuticals_theranostics_pet_cgmp_patch.py
 42. 2026-11-23_v6.2b_combination_products_drug_device_human_factors_patch.py
 43. 2026-11-23_v6.2c_complex_generics_nitrosamines_q3d_botanicals_patch.py
 44. 2026-11-24_v6.2d_drug_shortages_supply_resilience_essential_meds_patch.py
 45. 2026-11-24_v6.2e_amr_antibiotics_phage_carb_x_incentives_patch.py
 46. 2026-11-24_v6.2f_excipients_dmfs_nanomaterials_lai_patch.py
 47. 2026-11-24_v6.2g_oncology_oce_accelerated_approval_master_protocols_patch.py
 48. 2026-11-24_v6.2h_gcp_bimo_part11_cdisc_standards_patch.py
 49. 2026-11-24_v6.2i_adcs_bispecifics_peptides_oligonucleotides_patch.py
 50. 2026-11-24_v6.2j_rmat_hctp_cgt_potency_genome_editing_patch.py
 51. 2026-11-24_v6.2k_pfdd_coa_expanded_access_right_to_try_patch.py
 52. 2026-11-24_v6.2l_continuous_mfg_ich_q13_pat_etp_ai_mfg_patch.py
 53. 2026-11-24_v6.2m_analytical_q2_q14_usp_ich_q12_stability_patch.py
 54. 2026-11-24_v6.2n_nonclinical_safety_ich_m3_s1b_s6_s9_nams_patch.py
 55. 2026-11-24_v6.2o_bioequivalence_bcs_m9_nti_ivpt_pbpk_patch.py
 56. 2026-11-24_v6.2p_midd_ich_m15_poppk_exposure_response_qsp_patch.py
 57. 2026-11-24_v6.2q_drug_labeling_plr_spl_slc_rems_etasu_patch.py
 58. 2026-11-24_v6.2r_inspections_form483_recalls_fars_data_integrity_patch.py
 59. 2026-11-25_v6.2s_drug_discovery_hts_sbdd_protacs_alphafold_patch.py
 60. 2026-11-25_v6.2t_packaging_ccs_ich_q3e_el_dscsa_edds_patch.py
 61. 2026-11-26_v6.2u_user_fees_pdufa_gdufa_bsufa_omufa_prv_expedited_patch.py

Usage:
  python3 2026-11-26_apply_v6.1_unified_release_v57.py --selftest
  python3 2026-11-26_apply_v6.1_unified_release_v57.py \\
    --source-zip 2026-11-21_pill-by-pill-source_v6.0b.zip \\
    --patches-dir . \\
    --out-zip 2026-11-26_pill-by-pill-source_v6.1.zip
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

PATCH_ORDER = [
    ("v6.0a", "2026-11-20_v6.0a_vendors_cdmo_audit_comparator_patch.py"),
    ("v6.0b", "2026-11-20_v6.0b_pharma_encyclopedia_departments_patch.py"),
    ("v6.0c", "2026-11-20_v6.0c_equipment_market_pricing_patch.py"),
    ("v6.0_fetchers_wiring", "2026-11-21_v6.0_vendors_fetchers_and_route_wiring_patch.py"),
    ("v6.0_deep_depts_tests", "2026-11-21_v6.0_departments_deep_and_unified_tests_patch.py"),
    ("v6.0d_crosslinks_api", "2026-11-21_v6.0d_crosslinks_price_charts_and_api_patch.py"),
    ("v6.0e_rollups_oems_svg", "2026-11-21_v6.0e_parent_rollups_oem_matrix_and_lifecycle_svg_patch.py"),
    ("v6.0f_static_seo", "2026-11-21_v6.0f_static_seo_and_sitemap_patch.py"),
    ("v6.0g_equip_18", "2026-11-21_v6.0g_equipment_expansion_18_classes_patch.py"),
    ("v6.0h_origins75_browser_tests", "2026-11-21_v6.0h_origin_stories_batch7_and_v60_browser_tests_patch.py"),
    ("v6.0i_8stage_lifecycle", "2026-11-21_v6.0i_end_to_end_8stage_lifecycle_patch.py"),
    ("v6.0j_software_economics", "2026-11-21_v6.0j_pharma_software_and_economics_patch.py"),
    ("v6.0k_partner_ecosystem", "2026-11-21_v6.0k_partner_ecosystem_patch.py"),
    ("v6.0l_playbooks_quiz58", "2026-11-21_v6.0l_modality_playbooks_and_v60_quiz_patch.py"),
    ("v6.1a_global_search_origins_csv", "2026-11-22_v6.1a_global_search_origins_gallery_nav_csv_patch.py"),
    ("v6.1b_glossary_trace_ich", "2026-11-22_v6.1b_glossary_trace_storyboards_ich_patch.py"),
    ("v6.1c_chem_quiz_worksheets", "2026-11-22_v6.1c_chem_copy_quiz_filters_teacher_worksheets_patch.py"),
    ("v6.1d_grouped_nav_pointers_status", "2026-11-22_v6.1d_grouped_nav_clinical_pointers_feed_status_patch.py"),
    ("v6.1e_atc_tree_origins90", "2026-11-22_v6.1e_atc_class_tree_and_origins_batch8_patch.py"),
    ("v6.1f_gsc_fix_origins100_storyboards5", "2026-11-22_v6.1f_gsc_schema_fix_origins100_and_5modality_storyboards_patch.py"),
    ("v6.1g_seo_search_browser_coverage", "2026-11-22_v6.1g_seo_global_search_and_browser_test_coverage_patch.py"),
    ("v6.1h_pathways_exclusivity", "2026-11-22_v6.1h_regulatory_pathways_and_exclusivity_comparator_patch.py"),
    ("v6.1i_clinical_trials_endpoints", "2026-11-22_v6.1i_clinical_trial_design_and_endpoints_patch.py"),
    ("v6.1j_adme_pk_medchem_delivery", "2026-11-23_v6.1j_adme_pk_medchem_and_delivery_patch.py"),
    ("v6.1k_pharmacovigilance_safety", "2026-11-23_v6.1k_pharmacovigilance_and_drug_safety_patch.py"),
    ("v6.1l_ip_patents_hatch_waxman_bpcia", "2026-11-23_v6.1l_pharma_ip_patents_hatch_waxman_bpcia_patch.py"),
    ("v6.1m_sterile_bioprocessing_cleanroom", "2026-11-23_v6.1m_sterile_manufacturing_bioprocessing_cleanroom_patch.py"),
    ("v6.1n_global_reg_hta", "2026-11-23_v6.1n_global_regulatory_agencies_and_hta_comparator_patch.py"),
    ("v6.1o_cdx_biomarkers", "2026-11-23_v6.1o_companion_diagnostics_biomarkers_patch.py"),
    ("v6.1p_real_world_evidence", "2026-11-23_v6.1p_real_world_evidence_rwd_patch.py"),
    ("v6.1q_supply_chain_dscsa", "2026-11-23_v6.1q_supply_chain_dscsa_cold_chain_patch.py"),
    ("v6.1r_biologics_cgt", "2026-11-23_v6.1r_biologics_cgt_advanced_modalities_patch.py"),
    ("v6.1s_vaccines_adjuvants", "2026-11-23_v6.1s_vaccines_immunology_adjuvants_patch.py"),
    ("v6.1t_orphan_pediatric", "2026-11-23_v6.1t_rare_diseases_orphan_pediatric_access_patch.py"),
    ("v6.1u_digital_health_samd_dct", "2026-11-23_v6.1u_digital_health_samd_ai_ml_dct_patch.py"),
    ("v6.1v_otc_compounding_dshea", "2026-11-23_v6.1v_otc_monographs_switches_compounding_dshea_patch.py"),
    ("v6.1w_promotion_opdp_transparency", "2026-11-23_v6.1w_drug_promotion_opdp_transparency_patch.py"),
    ("v6.1x_controlled_substances_dea_rems", "2026-11-23_v6.1x_controlled_substances_dea_rems_patch.py"),
    ("v6.1y_pricing_ira_340b_mdrp", "2026-11-23_v6.1y_pharma_pricing_ira_340b_mdrp_patch.py"),
    ("v6.1z_special_populations_pllr", "2026-11-23_v6.1z_special_populations_pediatric_pllr_geriatric_diversity_patch.py"),
    ("v6.2a_radiopharma_theranostics", "2026-11-23_v6.2a_radiopharmaceuticals_theranostics_pet_cgmp_patch.py"),
    ("v6.2b_combo_products_hfe", "2026-11-23_v6.2b_combination_products_drug_device_human_factors_patch.py"),
    ("v6.2c_complex_quality_nitrosamines", "2026-11-23_v6.2c_complex_generics_nitrosamines_q3d_botanicals_patch.py"),
    ("v6.2d_shortages_resilience", "2026-11-24_v6.2d_drug_shortages_supply_resilience_essential_meds_patch.py"),
    ("v6.2e_amr_antiinfectives", "2026-11-24_v6.2e_amr_antibiotics_phage_carb_x_incentives_patch.py"),
    ("v6.2f_excipients_dmfs_nano", "2026-11-24_v6.2f_excipients_dmfs_nanomaterials_lai_patch.py"),
    ("v6.2g_oncology_oce", "2026-11-24_v6.2g_oncology_oce_accelerated_approval_master_protocols_patch.py"),
    ("v6.2h_gcp_bimo_cdisc", "2026-11-24_v6.2h_gcp_bimo_part11_cdisc_standards_patch.py"),
    ("v6.2i_adcs_bispecifics_oligos", "2026-11-24_v6.2i_adcs_bispecifics_peptides_oligonucleotides_patch.py"),
    ("v6.2j_rmat_hctp_cgt_cmc", "2026-11-24_v6.2j_rmat_hctp_cgt_potency_genome_editing_patch.py"),
    ("v6.2k_pfdd_coa_expanded_access", "2026-11-24_v6.2k_pfdd_coa_expanded_access_right_to_try_patch.py"),
    ("v6.2l_continuous_pat_ai_mfg", "2026-11-24_v6.2l_continuous_mfg_ich_q13_pat_etp_ai_mfg_patch.py"),
    ("v6.2m_analytical_usp_q12", "2026-11-24_v6.2m_analytical_q2_q14_usp_ich_q12_stability_patch.py"),
    ("v6.2n_nonclinical_nams", "2026-11-24_v6.2n_nonclinical_safety_ich_m3_s1b_s6_s9_nams_patch.py"),
    ("v6.2o_babe_bcs_nti", "2026-11-24_v6.2o_bioequivalence_bcs_m9_nti_ivpt_pbpk_patch.py"),
    ("v6.2p_midd_pharmacometrics", "2026-11-24_v6.2p_midd_ich_m15_poppk_exposure_response_qsp_patch.py"),
    ("v6.2q_labeling_spl_rems", "2026-11-24_v6.2q_drug_labeling_plr_spl_slc_rems_etasu_patch.py"),
    ("v6.2r_inspections_483_recalls", "2026-11-24_v6.2r_inspections_form483_recalls_fars_data_integrity_patch.py"),
    ("v6.2s_discovery_sbdd_protacs", "2026-11-25_v6.2s_drug_discovery_hts_sbdd_protacs_alphafold_patch.py"),
    ("v6.2t_packaging_el_dscsa", "2026-11-25_v6.2t_packaging_ccs_ich_q3e_el_dscsa_edds_patch.py"),
    ("v6.2u_user_fees_prv", "2026-11-26_v6.2u_user_fees_pdufa_gdufa_bsufa_omufa_prv_expedited_patch.py"),
    ("v6.2v_pv_faers_sentinel", "2026-11-26_v6.2v_pharmacovigilance_faers_sentinel_ich_e2_patch.py"),
    ("v6.2w_microbiology_sterility", "2026-11-26_v6.2w_pharma_microbiology_sterility_endotoxin_ccit_patch.py"),
]


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



def _sanitize_js_and_routes(root: pathlib.Path) -> dict:
    """Fix ./dom.js -> ./ui.js imports and move any post-route() lines in app.js before route()."""
    fixed_dom = []
    js_dir = root / "site" / "js"
    if js_dir.is_dir():
        for js_file in sorted(js_dir.glob("*.js")):
            src = js_file.read_text(encoding="utf-8")
            if 'from "./dom.js"' in src or "from './dom.js'" in src:
                new_src = src.replace('from "./dom.js"', 'from "./ui.js"').replace("from './dom.js'", "from './ui.js'")
                js_file.write_text(new_src, encoding="utf-8")
                fixed_dom.append(js_file.name)
    fixed_app_routes = False
    app_js = js_dir / "app.js"
    if app_js.is_file():
        app_src = app_js.read_text(encoding="utf-8")
        if "route();" in app_src:
            head, tail = app_src.split("route();", 1)
            tail_lines = tail.splitlines(keepends=True)
            moved = [l for l in tail_lines if 'if (path === "/ref/' in l or 'if (path === "/explore/' in l]
            kept = [l for l in tail_lines if l not in moved]
            if moved:
                app_js.write_text(head + "".join(moved) + "route();" + "".join(kept), encoding="utf-8")
                fixed_app_routes = True
    return {"fixed_dom_imports": fixed_dom, "fixed_post_route_lines": fixed_app_routes}

def _bump_version(root: pathlib.Path) -> list:
    bumped = []
    app_py = root / "app.py"
    if app_py.is_file():
        txt = app_py.read_text(encoding="utf-8")
        new_txt = re.sub(r'Pill by Pill v[56]\.\d+', 'Pill by Pill v6.1', txt)
        new_txt = re.sub(r'version="[56]\.\d+"', 'version="6.1"', new_txt)
        if new_txt != txt:
            app_py.write_text(new_txt, encoding="utf-8")
            bumped.append("app.py")
    ver_json = root / "site" / "version.json"
    if ver_json.is_file():
        try:
            v = json.loads(ver_json.read_text(encoding="utf-8"))
            v["version"] = "6.1"
            v["v60_modules"] = [
                "departments_8stage", "routes", "equipment_18", "software_stack_10",
                "economics_capital_gtn", "partner_ecosystem_6", "modality_playbooks_5",
                "quiz_58", "vendors", "route_links", "parent_rollups", "oem_matrix",
                "lab_kits_5", "lifecycle_svg_8stage", "static_seo_v61_30pages", "origins_100",
                "v61_browser_tests", "global_search_full", "origins_gallery", "csv_export",
                "acronym_glossary_24", "trace_storyboards_5", "ich_q1_q12_matrix",
                "chem_copy_tools", "quiz_topic_filters", "printable_worksheets_4",
                "grouped_ref_nav", "clinical_pointers", "feed_status_badges",
                "atc_class_tree", "gsc_medical_entity_schema", "regulatory_pathways_comparator",
                "clinical_trial_design_endpoints", "adme_pk_medchem_delivery",
                "pharmacovigilance_drug_safety", "pharma_ip_patents_hatch_waxman_bpcia",
                "sterile_manufacturing_bioprocessing_cleanroom", "global_reg_hta_comparator",
                "diagnostics_cdx_biomarkers", "real_world_evidence_rwd",
                "supply_chain_dscsa_cold_chain", "biologics_cgt_modalities",
                "vaccines_immunology_adjuvants", "orphan_pediatric_access",
                "digital_health_samd_dct", "otc_compounding_dshea",
                "promotion_transparency_compliance", "controlled_substances_dea_rems",
                "pricing_ira_340b_mdrp", "special_populations_pediatric_pllr_diversity",
                "radiopharma_theranostics_pet_cgmp", "combination_products_21cfr4_hfe",
                "complex_generics_nitrosamines_q3d_botanicals",
                "shortages_resilience_essential_meds",
                "amr_antibiotics_phage_incentives",
                "excipients_dmfs_nanomaterials",
                "oncology_oce_master_protocols",
                "gcp_bimo_part11_cdisc",
                "adcs_bispecifics_peptides_oligos",
                "rmat_hctp_cgt_potency_ge",
                "pfdd_coa_expanded_access",
                "continuous_pat_ai_mfg",
                "analytical_q2_q14_usp_ich_q12",
                "nonclinical_safety_glp_nams",
                "babe_bcs_m9_nti_ivpt_pbpk",
                "midd_ich_m15_poppk_er_qsp",
                "labeling_plr_spl_slc_rems",
                "inspections_483_recalls_alcoa",
                "discovery_qhts_sbdd_protacs",
                "packaging_ccs_ich_q3e_dscsa",
                "user_fees_pdufa_gdufa_prv_expedited",
                "pharmacovigilance_faers_sentinel_ich_e2",
                "microbiology_sterility_endotoxins_ccit",
            ]
            ver_json.write_text(json.dumps(v, indent=2) + "\n", encoding="utf-8")
            bumped.append("site/version.json")
        except Exception:
            pass
    return bumped


def integrate_v61(tree: pathlib.Path, patches_dir: pathlib.Path, raw_dir: pathlib.Path | None = None) -> dict:
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
    _sanitize_js_and_routes(tree)
    for bname, args in [
        ("build_departments.py", [str(data_dir)]),
        ("build_vendors.py", [str(raw_src), str(data_dir)]),
        ("build_equipment_catalog.py", [str(raw_src), str(data_dir)]),
        ("build_software_and_economics.py", [str(data_dir)]),
        ("build_partners.py", [str(data_dir)]),
        ("build_playbooks.py", [str(data_dir)]),
        ("build_origins_gallery.py", [str(tree / "pipeline" / "origin_stories.json"), str(data_dir)]),
        ("build_v61b_reference.py", [str(data_dir)]),
        ("build_worksheets.py", [str(data_dir)]),
        ("build_atc_tree.py", [str(data_dir)]),
        ("build_pathways.py", [str(data_dir)]),
        ("build_trials.py", [str(data_dir)]),
        ("build_adme.py", [str(data_dir)]),
        ("build_safety.py", [str(data_dir)]),
        ("build_ip_patents.py", [str(data_dir)]),
        ("build_sterile_mfg.py", [str(data_dir)]),
        ("build_global_reg_hta.py", [str(data_dir)]),
        ("build_diagnostics.py", [str(data_dir)]),
        ("build_rwe.py", [str(data_dir)]),
        ("build_supply_chain.py", [str(data_dir)]),
        ("build_biologics_cgt.py", [str(data_dir)]),
        ("build_vaccines.py", [str(data_dir)]),
        ("build_orphan.py", [str(data_dir)]),
        ("build_digital_health.py", [str(data_dir)]),
        ("build_otc_compounding.py", [str(data_dir)]),
        ("build_promotion_transparency.py", [str(data_dir)]),
        ("build_controlled_substances.py", [str(data_dir)]),
        ("build_pricing_access.py", [str(data_dir)]),
        ("build_special_populations.py", [str(data_dir)]),
        ("build_radiopharma.py", [str(data_dir)]),
        ("build_combo_products.py", [str(data_dir)]),
        ("build_complex_quality.py", [str(data_dir)]),
        ("build_shortages_resilience.py", [str(data_dir)]),
        ("build_amr_antiinfectives.py", [str(data_dir)]),
        ("build_excipients_dmfs_nano.py", [str(data_dir)]),
        ("build_oncology_oce.py", [str(data_dir)]),
        ("build_gcp_bimo_cdisc.py", [str(data_dir)]),
        ("build_adcs_bispecifics_oligos.py", [str(data_dir)]),
        ("build_rmat_hctp_cgt_cmc.py", [str(data_dir)]),
        ("build_pfdd_coa_expanded_access.py", [str(data_dir)]),
        ("build_continuous_pat_ai_mfg.py", [str(data_dir)]),
        ("build_analytical_usp_q12.py", [str(data_dir)]),
        ("build_nonclinical_nams.py", [str(data_dir)]),
        ("build_babe_bcs_nti.py", [str(data_dir)]),
        ("build_midd_pharmacometrics.py", [str(data_dir)]),
        ("build_labeling_spl_rems.py", [str(data_dir)]),
        ("build_inspections_483_recalls.py", [str(data_dir)]),
        ("build_discovery_sbdd_protacs.py", [str(data_dir)]),
        ("build_packaging_el_dscsa.py", [str(data_dir)]),
        ("build_user_fees_prv.py", [str(data_dir)]),
        ("build_pv_faers_sentinel.py", [str(data_dir)]),
        ("build_microbiology_sterility.py", [str(data_dir)]),
        ("build_global_search.py", [str(data_dir)]),
        ("build_v60_static_pages.py", [str(tree / "site")]),
    ]:
        bpath = tree / "pipeline" / bname
        if bpath.is_file():
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
        assert v["version"] == "6.1" and "microbiology_sterility_endotoxins_ccit" in v["v60_modules"] and len(PATCH_ORDER) == 63

        out_zip = root / "clean_v6.1.zip"
        cnt = _pack_clean(tree, out_zip)
        assert cnt == 2, cnt
        with zipfile.ZipFile(out_zip, "r") as z:
            names = z.namelist()
            assert "app.py" in names and "site/version.json" in names
            assert not any("__pycache__" in n or n.endswith(".pyc") for n in names)
        print("V61_UNIFIED_INTEGRATOR_V57_SELFTEST_PASSED", json.dumps({"files_packed": cnt, "patches_in_order": len(PATCH_ORDER)}))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply all Pill by Pill v6.0a-l + v6.1a-z + v6.2a-u patches and build clean v6.1 source zip.")
    ap.add_argument("--source-zip", type=pathlib.Path, help="Input v6.0b or v5.26 source zip")
    ap.add_argument("--source-dir", type=pathlib.Path, help="Input unpacked source directory (alternative to --source-zip)")
    ap.add_argument("--patches-dir", type=pathlib.Path, default=pathlib.Path("."), help="Directory holding the patch scripts")
    ap.add_argument("--raw-dir", type=pathlib.Path, help="Optional raw/ directory with live FDA/USAspending/EMA JSON feeds")
    ap.add_argument("--out-zip", type=pathlib.Path, help="Output clean v6.1 source zip path")
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

        summary = integrate_v61(tree, args.patches_dir, args.raw_dir)
        if args.out_zip:
            summary["files_packed"] = _pack_clean(tree, args.out_zip)
            summary["out_zip"] = str(args.out_zip)
        print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
