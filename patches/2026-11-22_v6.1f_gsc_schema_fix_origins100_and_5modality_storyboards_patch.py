#!/usr/bin/env python3
"""Pill by Pill v6.1f Patch: Google Search Console Schema Fix (Drug -> MedicalEntity), Origin Stories Batch 9 (90 -> 100) & Complete 5-Modality Trace Storyboards (3 -> 5).

1. Fixes Google Search Console "Product snippets structured data issues (missing offers/review/aggregateRating)"
   by updating `pipeline/build_static_pages.py` to emit `"@type": "MedicalEntity"` instead of
   `"@type": "Drug"` (since Schema.org `Drug` inherits from `Product`).
2. Appends 10 primary-sourced landmark origin stories (Batch 9, checked 2026-11-22 against PMC)
   to `pipeline/origin_stories.json` (90 -> 100 total, idempotently deduplicated).
3. Appends 2 End-to-End Trace-One-Drug Storyboards (Pembrolizumab mAb + Tisagenlecleucel CAR-T)
   to `pipeline/build_v61b_reference.py` so all 5 pharmaceutical modalities have full 8-stage
   storyboards (3 -> 5 total).

Usage:
  python3 2026-11-22_v6.1f_gsc_schema_fix_origins100_and_5modality_storyboards_patch.py --selftest
  python3 2026-11-22_v6.1f_gsc_schema_fix_origins100_and_5modality_storyboards_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

BATCH9_ORIGINS = [{'medicine': 'SERTRALINE', 'category': 'Selective receptor design', 'simple': 'In the late 1970s, Pfizer scientists including B. Kenneth Koe designed sertraline (Zoloft) to selectively block serotonin reuptake while avoiding the anticholinergic and heart side effects of older tricyclic antidepressants.', 'expert': 'Co-invented at Pfizer in the late 1970s by B. Kenneth Koe and colleagues (reported 1983), sertraline was engineered as a selective serotonin reuptake inhibitor (SSRI) lacking norepinephrine reuptake, monoamine oxidase, and significant anticholinergic activity.', 'sources': [{'label': 'PMC5101563 — B. Kenneth Koe (Sertraline co-inventor)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC5101563/'}, {'label': 'PMC4163971 — Sertraline pharmacology background (citing Koe 1983)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4163971/'}], 'checked': '2026-11-22'}, {'medicine': 'PROPOFOL', 'category': 'Medicinal chemistry', 'simple': "Veterinarian and researcher John 'Iain' Glen at ICI discovered and formulated propofol—solving how to dissolve the oily anesthetic in a milky soybean-oil emulsion so patients fall asleep smoothly and wake up quickly, earning the 2018 Lasker Award.", 'expert': 'Discovered at ICI (now part of AstraZeneca) and developed by John (Iain) Glen, propofol (2,6-diisopropylphenol) was formulated as a lipid emulsion intravenous anesthetic with rapid onset and recovery, recognized with the 2018 Lasker-DeBakey Clinical Medical Research Award.', 'sources': [{'label': 'PMC6159986 — The 2018 Lasker-DeBakey Award (Iain Glen & Propofol)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6159986/'}, {'label': 'PMC8329483 — Propofol discovery at ICI', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8329483/'}], 'checked': '2026-11-22'}, {'medicine': 'SUMATRIPTAN', 'category': 'Selective receptor design', 'simple': "At Glaxo, Patrick Humphrey and colleagues modified serotonin to create sumatriptan (Imitrex), the first 'triptan' medicine designed specifically to calm dilated blood vessels and pain pathways during migraine and cluster headaches.", 'expert': 'Developed at Glaxo by Patrick Humphrey and colleagues as the prototypical triptan, sumatriptan (Imigran/Imitrex) was engineered as a selective serotonin 5-HT1B/1D receptor agonist for acute migraine and cluster headache.', 'sources': [{'label': 'PMC3635591 — Sir David Jack & Glaxo drug discovery (Patrick Humphrey)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC3635591/'}, {'label': 'PMC1760750 — Neuropharmacology of 5-hydroxytryptamine (prototypical triptan)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC1760750/'}], 'checked': '2026-11-22'}, {'medicine': 'SITAGLIPTIN', 'category': 'Rational enzyme inhibitor', 'simple': "After scientists discovered that the enzyme DPP-4 rapidly breaks down the body's own blood-sugar hormone GLP-1, Nancy Thornberry and Ann Weber's team at Merck designed sitagliptin (approved 2006)—the first oral DPP-4 inhibitor pill for type 2 diabetes.", 'expert': 'Developed at Merck Sharp & Dohme by a team led by Nancy Thornberry and Ann Weber, sitagliptin (Januvia) became the first FDA-approved selective dipeptidyl peptidase-4 (DPP-4) inhibitor in 2006, prolonging endogenous GLP-1 activity in type 2 diabetes.', 'sources': [{'label': 'PMC11441540 — Discovery and development of GLP-1 based drugs', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11441540/'}, {'label': 'PMC4449938 — The Place of Dipeptidyl Peptidase-4 Inhibitors in Type 2 Diabetes', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4449938/'}], 'checked': '2026-11-22'}, {'medicine': 'RIVAROXABAN', 'category': 'Rational enzyme inhibitor', 'simple': "Seeking a predictable oral blood thinner that would not require warfarin's constant blood tests, Bayer scientists including Elisabeth Perzborn developed rivaroxaban (BAY 59-7939)—one of the first direct oral Factor Xa inhibitors.", 'expert': 'Discovered at Bayer (BAY 59-7939) with preclinical pharmacological characterization led by Elisabeth Perzborn and colleagues, rivaroxaban was developed as a once-daily oral direct coagulation Factor Xa inhibitor for thromboprophylaxis, DVT/PE, and atrial fibrillation.', 'sources': [{'label': 'PMC3838992 — The discovery of rivaroxaban: translating preclinical assessments', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC3838992/'}, {'label': 'PMC11466925 — Direct oral Factor Xa inhibitors', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11466925/'}], 'checked': '2026-11-22'}, {'medicine': 'OSIMERTINIB', 'category': 'Structure-guided covalent design', 'simple': 'When lung cancer tumors evolved a resistance mutation (T790M) that blocked earlier EGFR pills, AstraZeneca chemists at Alderley Park launched a 2009 project to build osimertinib—an irreversible covalent inhibitor that spares healthy EGFR and earned FDA approval in 2015.', 'expert': "Initiated in May 2009 at AstraZeneca's Alderley Park research site using structure-based design for irreversible covalent inhibitors, osimertinib selectively targets sensitizing and T790M-mutant EGFR over wild-type EGFR, earning accelerated FDA approval in 2015.", 'sources': [{'label': 'PMC6072417 — Discovery of osimertinib at AstraZeneca (Alderley Park)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6072417/'}, {'label': 'PMC5995494 — Osimertinib: Overcoming T790M Mutations in NSCLC', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC5995494/'}], 'checked': '2026-11-22'}, {'medicine': 'GABAPENTIN', 'category': 'Rational analog', 'simple': 'Developed by Parke-Davis and first approved by the FDA in 1993 as Neurontin for partial seizures, gabapentin was later expanded to treat nerve pain after shingles (postherpetic neuralgia).', 'expert': 'Developed by Parke-Davis and initially approved by the FDA in 1993 (Neurontin) as adjunctive therapy for partial seizures, gabapentin was subsequently approved for postherpetic neuralgia.', 'sources': [{'label': 'PMC6153543 — Gabapentin history and FDA approval (1993)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6153543/'}, {'label': 'PMC9643740 — Drug reprofiling history (gabapentin)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9643740/'}], 'checked': '2026-11-22'}, {'medicine': 'LENALIDOMIDE', 'category': 'Immunomodulatory analog', 'simple': 'After researchers found that thalidomide could fight blood cancers and quiet TNF-alpha, chemists added an amino group to its ring to create lenalidomide (CC-5013)—a far more potent oral medicine for multiple myeloma and 5q- myelodysplastic syndrome.', 'expert': 'Created as a 4-amino phthaloyl analogue of thalidomide (CC-5013) lacking one carbonyl group, lenalidomide was developed by Celgene as a first-in-class immunomodulatory imide drug (IMiD) that binds cereblon (CRBN) to trigger targeted degradation of transcription factors and CK1-alpha in multiple myeloma and del(5q) MDS.', 'sources': [{'label': 'PMC3922408 — Mechanism of action of immunomodulatory drugs (IMiDs)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC3922408/'}, {'label': 'PMC7298168 — Molecular mechanisms of thalidomide and its derivatives (CRBN)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7298168/'}], 'checked': '2026-11-22'}, {'medicine': 'ALENDRONATE SODIUM', 'category': 'Repurposed industrial chemistry', 'simple': "Bisphosphonates began as industrial 'water softeners' related to pyrophosphate that stop calcium crystals from forming or dissolving—leading scientists to turn them into bone-protecting pills like alendronate, FDA-approved for osteoporosis in 1995.", 'expert': "Tracing back to Herbert Fleisch and colleagues' discovery that pyrophosphate and synthetic bisphosphonates inhibit hydroxyapatite dissolution and osteoclast-mediated bone resorption, alendronate became a pioneering oral bisphosphonate FDA-approved for osteoporosis in 1995.", 'sources': [{'label': 'PMC7665836 — Osteoporosis: Mechanism, Molecular Target, and Current Status', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7665836/'}, {'label': 'PMC10940084 — Bisphosphonates for osteoporosis: from bench to clinic', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10940084/'}], 'checked': '2026-11-22'}, {'medicine': 'NIRMATRELVIR', 'category': 'Structure-guided covalent design', 'simple': 'During the COVID-19 pandemic, Pfizer chemists started from an intravenous SARS-CoV-1 compound made over 15 years earlier and redesigned it with a nitrile warhead into nirmatrelvir—an oral antiviral pill paired with ritonavir (Paxlovid) authorized in December 2021.', 'expert': "Engineered by Pfizer (PF-07321332) from the earlier intravenous SARS-CoV-1 main protease (Mpro) inhibitor PF-00835231 by reducing hydrogen-bond donors and introducing a P1' nitrile warhead that forms a reversible covalent thioimidate adduct with Cys145, nirmatrelvir (co-packaged with ritonavir as Paxlovid) received FDA EUA on December 22, 2021.", 'sources': [{'label': 'PMC9425786 — The history, mechanism, and perspectives of nirmatrelvir (PF-07321332)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9425786/'}, {'label': 'PMC10891713 — The Design, Synthesis and Mechanism of Action of Paxlovid', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10891713/'}], 'checked': '2026-11-22'}]
EXTRA_STORYBOARDS_2 = [{'id': 'pembrolizumab', 'drug_name': 'Pembrolizumab (Keytruda)', 'drug_slug': 'pembrolizumab', 'modality': 'Monoclonal Antibody (mAb)', 'headline': "Releasing the PD-1 immune brake so a patient's own T cells attack cancer", 'plain_intro': 'Follow how a humanized antibody grown in living mammalian cells transformed cancer immunotherapy across dozens of tumor types.', 'stages': [{'stage_id': 'discovery', 'label': '1. Discovery', 'summary': 'Built on immune checkpoint biology (PD-1/PD-L1); originally engineered at Organon/Schering-Plough and humanized as an IgG4-kappa monoclonal antibody blocking PD-1 without triggering Fc-mediated T-cell depletion.'}, {'stage_id': 'formulation', 'label': '2. Formulation', 'summary': 'Formulated as a sterile single-dose aqueous IV infusion solution (and later subcutaneous formulation) stabilized with histidine buffer, sucrose, and polysorbate 80.'}, {'stage_id': 'analytical', 'label': '3. Analytical QC', 'summary': 'Characterized for charge variants (icIEF), aggregates (SEC-UPLC), intact mass & peptide mapping (LC-MS), glycosylation profile, cell-based potency, and sterility/endotoxin.'}, {'stage_id': 'clinical', 'label': '4. Clinical Trials', 'summary': 'KEYNOTE-001 through hundreds of global trials demonstrated durable survival gains in melanoma, NSCLC, and MSI-H tumors—including the first tissue-agnostic biomarker cancer approval.'}, {'stage_id': 'regulatory', 'label': '5. Regulatory', 'summary': 'Approved by FDA in September 2014 (BLA 125514) under Breakthrough Therapy and Accelerated Approval pathways, followed by EMA, Health Canada, and PMDA.'}, {'stage_id': 'manufacturing', 'label': '6. Manufacturing', 'summary': 'Fed-batch CHO mammalian cell culture in large bioreactors, Protein A affinity & polishing chromatography, ICH Q5A viral clearance, TFF/UFDF concentration, and ISO 5 aseptic vial fill-finish.'}, {'stage_id': 'commercial', 'label': '7. Economics & IP', 'summary': 'Protected by Purple Book 12-year reference biologic exclusivity and layered formulation/indication patents; reimbursed largely via Medicare Part B buy-and-bill and commercial medical benefits.'}, {'stage_id': 'distribution', 'label': '8. Distribution & Safety', 'summary': '2–8°C continuous cold-chain 3PLs and specialty distributors to oncology infusion centers, with ongoing pharmacovigilance for immune-mediated adverse events.'}], 'sources': [{'label': 'PMC5010088 — Pembrolizumab discovery & development', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC5010088/'}, {'label': 'FDA — Step 3: Clinical Research', 'url': 'https://www.fda.gov/patients/drug-development-process/step-3-clinical-research'}]}, {'id': 'tisagenlecleucel', 'drug_name': 'Tisagenlecleucel (Kymriah)', 'drug_slug': 'tisagenlecleucel', 'modality': 'Cell & Gene Therapy (Autologous CAR-T)', 'headline': "Reprogramming a patient's own T cells into a living, one-time leukemia therapy", 'plain_intro': "Trace how a patient's white blood cells are collected at a hospital, genetically engineered in a cleanroom, frozen in liquid nitrogen, and infused back as a living medicine.", 'stages': [{'stage_id': 'discovery', 'label': '1. Discovery', 'summary': 'Pioneered by Carl June and colleagues at the University of Pennsylvania using a lentiviral vector encoding an anti-CD19 Chimeric Antigen Receptor (CAR) with a 4-1BB costimulatory domain.'}, {'stage_id': 'formulation', 'label': '2. Formulation', 'summary': 'Formulated as a patient-specific cryopreserved sterile cell suspension in DMSO-containing cryoprotectant infusion bags thawed at the hospital bedside.'}, {'stage_id': 'analytical', 'label': '3. Analytical QC', 'summary': 'Every individual patient lot undergoes rapid sterility, mycoplasma, endotoxin, cell viability, % CAR-positive flow cytometry, vector copy number (VCN), and replication-competent lentivirus (RCL) testing.'}, {'stage_id': 'clinical', 'label': '4. Clinical Trials', 'summary': 'Pivotal ELIANA (pediatric/young-adult B-ALL) and JULIET (DLBCL) multicenter trials demonstrated high complete remission rates in relapsed/refractory patients, with mandatory 15-year long-term safety follow-up.'}, {'stage_id': 'regulatory', 'label': '5. Regulatory', 'summary': 'Approved by FDA CBER in August 2017 (BLA 125646)—the first gene therapy / CAR-T cell therapy approved in the United States—under Breakthrough Therapy and Priority Review.'}, {'stage_id': 'manufacturing', 'label': '6. Manufacturing', 'summary': "Autologous 'vein-to-vein' batch-of-one processing: hospital leukapheresis -> cryopreservation -> lentiviral transduction & T-cell expansion in cleanrooms -> washing, cryopreservation, and QC release."}, {'stage_id': 'commercial', 'label': '7. Economics & IP', 'summary': 'One-time curative pricing model paired with outcomes-based agreements, hospital DRG/NTAP reimbursement, and CMS Cell & Gene Therapy Access initiatives.'}, {'stage_id': 'distribution', 'label': '8. Distribution & Safety', 'summary': 'Cryogenic liquid-nitrogen (<-150°C) specialty couriers with strict Chain of Identity (COI) tracking and REMS-certified treatment centers trained to manage cytokine release syndrome (CRS).'}], 'sources': [{'label': 'FDA — First Gene Therapy Approval (Kymriah, 2017)', 'url': 'https://www.fda.gov/news-events/press-announcements/fda-approval-brings-first-gene-therapy-united-states'}, {'label': 'FDA — Step 5: Post-Market Safety Monitoring', 'url': 'https://www.fda.gov/patients/drug-development-process/step-5-fda-post-market-drug-safety-monitoring'}]}]


def _patch_static_pages_schema(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    new_txt = txt.replace('"@type": "Drug"', '"@type": "MedicalEntity"').replace("'@type': 'Drug'", "'@type': 'MedicalEntity'")
    if new_txt != txt:
        path.write_text(new_txt, encoding="utf-8")
        return True
    return False


def _patch_origin_stories(path: pathlib.Path) -> int:
    if not path.is_file():
        return 0
    doc = json.loads(path.read_text(encoding="utf-8"))
    stories = doc.get("stories") if isinstance(doc, dict) else doc
    if not isinstance(stories, list):
        raise ValueError(f"Unexpected origin_stories.json structure in {path}")
    existing = {str(s.get("medicine", "")).strip().upper() for s in stories}
    added = 0
    for entry in BATCH9_ORIGINS:
        key = entry["medicine"].strip().upper()
        if key not in existing:
            stories.append(entry)
            existing.add(key)
            added += 1
    if added:
        if isinstance(doc, dict):
            doc["stories"] = stories
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        else:
            path.write_text(json.dumps(stories, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return added


def _patch_storyboards_builder(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"tisagenlecleucel"' in txt:
        return False
    anchor = "def build_v61b_reference("
    if anchor not in txt:
        return False
    add_block = (
        "\n# v6.1f: Complete 5-modality Trace-One-Drug storyboards (+mAb, +CAR-T -> 5 total)\n"
        "_V61F_EXTRA_STORYBOARDS = " + json.dumps(EXTRA_STORYBOARDS_2, indent=4, ensure_ascii=False) + "\n"
        "for _sb in _V61F_EXTRA_STORYBOARDS:\n"
        "    if not any(x.get('id') == _sb['id'] for x in TRACE_STORYBOARDS):\n"
        "        TRACE_STORYBOARDS.append(_sb)\n\n"
    )
    path.write_text(txt.replace(anchor, add_block + anchor, 1), encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    return {
        "gsc_schema_drug_to_medical_entity": _patch_static_pages_schema(pipe_dir / "build_static_pages.py"),
        "batch9_origin_stories_added": _patch_origin_stories(pipe_dir / "origin_stories.json"),
        "storyboards_expanded_to_5": _patch_storyboards_builder(pipe_dir / "build_v61b_reference.py"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "data").mkdir(parents=True)

        (root / "pipeline" / "build_static_pages.py").write_text(
            'ld = {"@type": "MedicalWebPage", "about": {"@type": "Drug", "name": "Aspirin"}}\n',
            encoding="utf-8",
        )
        seed = {"stories": [{"medicine": f"DRUG_{i}", "category": "Test", "simple": "a", "expert": "b", "sources": [{"label": "s", "url": "https://example.org"}], "checked": "2026-11-22"} for i in range(90)]}
        (root / "pipeline" / "origin_stories.json").write_text(json.dumps(seed), encoding="utf-8")
        (root / "pipeline" / "build_v61b_reference.py").write_text(
            'import json, pathlib, sys\n'
            'TRACE_STORYBOARDS = [{"id": "imatinib"}, {"id": "semaglutide"}, {"id": "patisiran"}]\n'
            'def build_v61b_reference(d):\n'
            '    (pathlib.Path(d) / "trace_storyboards.json").write_text(json.dumps({"count": len(TRACE_STORYBOARDS), "storyboards": TRACE_STORYBOARDS}), encoding="utf-8")\n'
            'if __name__ == "__main__": build_v61b_reference(sys.argv[1])\n',
            encoding="utf-8",
        )

        r1 = apply_patch(root)
        assert r1["gsc_schema_drug_to_medical_entity"] and r1["batch9_origin_stories_added"] == 10 and r1["storyboards_expanded_to_5"], r1
        r2 = apply_patch(root)
        assert not r2["gsc_schema_drug_to_medical_entity"] and r2["batch9_origin_stories_added"] == 0 and not r2["storyboards_expanded_to_5"], r2

        sp_txt = (root / "pipeline" / "build_static_pages.py").read_text(encoding="utf-8")
        assert '"@type": "MedicalEntity"' in sp_txt and '"@type": "Drug"' not in sp_txt

        doc = json.loads((root / "pipeline" / "origin_stories.json").read_text(encoding="utf-8"))
        assert len(doc["stories"]) == 100, len(doc["stories"])
        for s in doc["stories"][-10:]:
            assert s["checked"] == "2026-11-22" and all(u["url"].startswith("https://") for u in s["sources"])

        subprocess.run([sys.executable, str(root / "pipeline" / "build_v61b_reference.py"), str(root / "site" / "data")], check=True)
        sb = json.loads((root / "site" / "data" / "trace_storyboards.json").read_text(encoding="utf-8"))
        assert sb["count"] == 5, sb

        print("V61F_GSC_SCHEMA_ORIGINS100_STORYBOARDS5_SELFTEST_PASSED", json.dumps({"total_stories": len(doc["stories"]), "total_storyboards": sb["count"], **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1f GSC Schema Fix, Origins Batch 9 (100) & 5-Modality Storyboards patch.")
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
