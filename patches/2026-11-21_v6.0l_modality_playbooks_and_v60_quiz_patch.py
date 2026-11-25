#!/usr/bin/env python3
"""Pill by Pill v6.0l Patch: Modality Playbooks (5 Modalities x 8 Stages) & v6.0 Pharma Operations Quiz Expansion (+8 -> 58 Questions).

1. Adds `pipeline/build_playbooks.py` -> `site/data/playbooks.json` comparing Small Molecule,
   Monoclonal Antibody (mAb), Therapeutic Peptide, Oligonucleotide/mRNA-LNP, and Cell & Gene
   Therapy across all 8 end-to-end lifecycle stages.
2. Adds `site/js/playbooks.js` (`playbooksPage`, `playbooksExplorePage`) and wires
   `#/ref/playbooks`, `#/explore/playbooks`, `/api/playbooks`, and `pipeline/run_all.sh`.
3. Appends 8 primary-sourced Pharma Operations quiz questions to `pipeline/quiz_extra.json`
   (bringing total quiz coverage from 50 -> 58 questions, idempotently deduplicated by question text).

Usage:
  python3 2026-11-21_v6.0l_modality_playbooks_and_v60_quiz_patch.py --selftest
  python3 2026-11-21_v6.0l_modality_playbooks_and_v60_quiz_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_PLAYBOOKS_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.0l Modality Playbooks dataset (`site/data/playbooks.json`).\n\nCompares the 5 core pharmaceutical modalities side-by-side across all 8 end-to-end\nlifecycle stages (Discovery, Formulation, Analytical QC, Clinical Trials, Regulatory,\nManufacturing, IP/Economics, and Distribution/Safety):\n  1. Small Molecule (Oral NCE)\n  2. Monoclonal Antibody (mAb)\n  3. Therapeutic Peptide\n  4. Oligonucleotide & mRNA-LNP (ASO / siRNA / mRNA)\n  5. Cell & Gene Therapy (AAV / CAR-T)\n\nAll regulatory anchors are verified HTTPS primary sources (FDA, eCFR, ICH).\n\nUsage:\n  python3 pipeline/build_playbooks.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-21"\n\nSTAGES = [\n    ("discovery", "1. Discovery & Preclinical"),\n    ("formulation", "2. Formulation & Route"),\n    ("analytical", "3. Analytical QC"),\n    ("clinical", "4. Clinical Trials"),\n    ("regulatory", "5. Regulatory & Approval"),\n    ("manufacturing", "6. Commercial Manufacturing"),\n    ("commercial", "7. IP, Pricing & Access"),\n    ("distribution", "8. Supply Chain & Safety"),\n]\n\nPLAYBOOKS = [\n    {\n        "id": "small-molecule",\n        "name": "Small Molecule (Oral NCE)",\n        "mw_range": "< 500–900 Da (synthetic chemical)",\n        "plain_summary": "Classic chemical medicines made by step-by-step lab synthesis and usually pressed into shelf-stable pills or capsules.",\n        "catalogue_filter": "#/ref/drugs?type=sm",\n        "stages": {\n            "discovery": "High-throughput screening (HTS), structure-based drug design (SBDD), medicinal chemistry SAR, and ADME/CYP450 screening.",\n            "formulation": "Oral solid dosage (tablets/capsules), salt/polymorph selection, amorphous solid dispersions (spray drying) for poorly soluble APIs.",\n            "analytical": "HPLC/UPLC assay & impurities (ICH Q3A/Q3B), dissolution testing (USP <711>), Karl Fischer moisture, ICP-MS elemental impurities (ICH Q3D).",\n            "clinical": "Healthy-volunteer Phase 1 SAD/MAD + food-effect & DDI studies; Phase 2 dose-ranging; Phase 3 multicenter RCTs.",\n            "regulatory": "FDA NDA under FD&C Act § 505(b)(1) or 505(b)(2) (21 CFR Part 314); generic entry via ANDA § 505(j) bioequivalence.",\n            "manufacturing": "Multi-step chemical synthesis in batch/continuous reactors, crystallization, milling, fluid-bed granulation, and rotary tablet presses.",\n            "commercial": "Orange Book patents + 5-year NCE exclusivity; rapid steep price drop (~80–90%) upon AB-rated generic entry (LOE).",\n            "distribution": "Ambient 15–25°C full-line wholesaler distribution (McKesson/Cencora/Cardinal) to retail pharmacies; DSCSA 2D serialization.",\n        },\n        "key_equipment": ["eq-hts-liquid-handler", "eq-hplc-uplc", "eq-dissolution-bath", "eq-spray-dryer", "eq-rotary-tablet-press"],\n        "sources": [\n            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314",\n            "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research",\n        ],\n    },\n    {\n        "id": "monoclonal-antibody",\n        "name": "Monoclonal Antibody (mAb)",\n        "mw_range": "~150,000 Da (recombinant glycoprotein)",\n        "plain_summary": "Large, Y-shaped proteins grown inside living mammalian cells that lock onto a specific disease target and are delivered by IV infusion or under-the-skin injection.",\n        "catalogue_filter": "#/ref/drugs?type=ab",\n        "stages": {\n            "discovery": "Hybridoma, phage display, or transgenic mouse discovery; humanization, affinity maturation, and Fc-engineering.",\n            "formulation": "Sterile liquid or lyophilized injectable (IV infusion or high-concentration subcutaneous autoinjector) with buffers and surfactants (polysorbate).",\n            "analytical": "Charge variants (icIEF/IEX), aggregates (SEC-UPLC), intact/peptide-map LC-MS, glycosylation profiling, cell-based potency, and endotoxin/sterility.",\n            "clinical": "Patient-based Phase 1/2 (especially oncology/immunology), immunogenicity (ADA/NAb) monitoring, and large Phase 3 outcomes trials.",\n            "regulatory": "FDA BLA under PHS Act § 351(a); biosimilar entry via § 351(k) analytical & clinical comparability (Purple Book).",\n            "manufacturing": "CHO cell-line master cell bank -> single-use or stainless-steel bioreactors -> Protein A affinity & polishing chromatography -> viral clearance (ICH Q5A) -> aseptic fill-finish.",\n            "commercial": "Purple Book 12-year reference biologic exclusivity + formulation/process patents; gradual biosimilar erosion via PBM formulary competition.",\n            "distribution": "2–8°C continuous cold-chain 3PLs, buy-and-bill infusion clinics (Medicare Part B), and Specialty Pharmacies.",\n        },\n        "key_equipment": ["eq-single-use-bioreactor", "eq-prep-chromatography", "eq-tff-skid", "eq-sterile-fill-finish", "eq-lyophilizer"],\n        "sources": [\n            "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research",\n            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211",\n        ],\n    },\n    {\n        "id": "peptide",\n        "name": "Therapeutic Peptide",\n        "mw_range": "~500–5,000 Da (up to ~40 amino acids)",\n        "plain_summary": "Short chains of amino acids that mimic natural body hormones (like GLP-1 or insulin)—chemically engineered to last longer in blood instead of breaking down in minutes.",\n        "catalogue_filter": "#/ref/drugs?type=pr",\n        "stages": {\n            "discovery": "Natural hormone templates, phage/mRNA display, backbone/non-canonical amino acid substitution (e.g., Aib), and fatty-acid acylation for albumin binding.",\n            "formulation": "Sterile subcutaneous pen injectors (preserved multi-dose cartridges) or permeation-enhanced oral tablets (e.g., SNAC).",\n            "analytical": "RP-HPLC/UPLC for closely related deletion/racemization impurities, HRMS peptide mapping, amino acid analysis, and bioassay potency.",\n            "clinical": "PK/PD biomarker-rich Phase 1/2 (e.g., glucose/weight/hormone curves) followed by large cardiovascular/metabolic outcomes Phase 3 trials.",\n            "regulatory": "FDA NDA (peptides <= 40 amino acids regulated as drugs under FD&C Act; >40 aa regulated as biologics under PHS Act § 351).",\n            "manufacturing": "Solid-phase peptide synthesis (SPPS), liquid-phase synthesis (LPPS), or recombinant fermentation; preparative RP-HPLC purification and lyophilization.",\n            "commercial": "Orange Book patents on sequence, delivery pen device, and salt/formulation; high-volume chronic payer/PBM rebate competition.",\n            "distribution": "2–8°C cold-chain warehousing/wholesalers to retail and mail-order pharmacies; pen-device supply-chain capacity is a major bottleneck.",\n        },\n        "key_equipment": ["eq-hplc-uplc", "eq-lc-ms-ms", "eq-lyophilizer", "eq-sterile-fill-finish"],\n        "sources": [\n            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314",\n            "https://www.fda.gov/patients/drug-development-process/step-5-fda-post-market-drug-safety-monitoring",\n        ],\n    },\n    {\n        "id": "oligonucleotide",\n        "name": "Oligonucleotide & mRNA-LNP (ASO / siRNA / mRNA)",\n        "mw_range": "~6,000–15,000 Da (ASO/siRNA) to >1 MDa (mRNA)",\n        "plain_summary": "Programmable genetic strands that silence or rewrite faulty protein instructions inside cells, protected by chemical backbones or microscopic fat bubbles (LNPs).",\n        "catalogue_filter": "#/ref/drugs?type=ol",\n        "stages": {\n            "discovery": "Sequence-based Watson-Crick target design, off-target transcriptome screening, phosphorothioate/2\'-MOE/2\'-F chemistry, and GalNAc or LNP targeting.",\n            "formulation": "Aqueous subcutaneous/intrathecal solution (GalNAc-siRNA / ASO) or microfluidic Lipid Nanoparticle (LNP) encapsulation (siRNA / mRNA).",\n            "analytical": "Ion-pair RP-LC-MS for n-1/n+1 sequence impurities, duplex integrity, LNP particle size (DLS) & encapsulation efficiency, and residual solvent/lipid assays.",\n            "clinical": "Target-biomarker knockdown in Phase 1 (e.g., hepatic protein or CSF biomarker) enabling rapid Phase 2/3 rare-disease or cardiometabolic trials.",\n            "regulatory": "FDA NDA for chemically synthesized ASOs/siRNAs; BLA for mRNA vaccines/biologics; frequent Orphan Drug & Breakthrough Therapy designations.",\n            "manufacturing": "Automated solid-phase oligonucleotide synthesis (phosphoramidite chemistry) or in vitro transcription (IVT), TFF ultrafiltration, and microfluidic LNP mixing.",\n            "commercial": "Composition, chemical-modification, and LNP lipid patent estates; often specialty-priced rare-disease or chronic biannual cardiometabolic access.",\n            "distribution": "2–8°C for GalNAc conjugates; -20°C to -80°C ultra-low-temperature cold-chain 3PLs for LNP/mRNA products; Specialty Pharmacies & clinics.",\n        },\n        "key_equipment": ["eq-microfluidic-lnp", "eq-tff-skid", "eq-lc-ms-ms", "eq-sterile-fill-finish"],\n        "sources": [\n            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314",\n            "https://www.fda.gov/media/77516/download",\n        ],\n    },\n    {\n        "id": "cell-gene-therapy",\n        "name": "Cell & Gene Therapy (AAV / CAR-T / CRISPR)",\n        "mw_range": "Viral vector (~4–5 MDa) or living engineered human cells",\n        "plain_summary": "Living cells or harmless viral carriers that deliver a working gene or reprogram a patient\'s own immune cells to fight cancer or genetic disease—often as a one-time treatment.",\n        "catalogue_filter": "#/ref/drugs?type=gc",\n        "stages": {\n            "discovery": "Viral capsid tropism engineering (AAV/lentivirus), CAR construct design, or CRISPR guide-RNA screening for on-target editing and zero off-target cuts.",\n            "formulation": "Cryopreserved sterile suspension in DMSO-containing cryoprotectant bags or vials ready for rapid bedside thaw and infusion.",\n            "analytical": "Vector genome titer (ddPCR), empty-to-full capsid ratio, replication-competent virus (RCL/RCA) safety, cell viability/phenotyping (flow cytometry), and rapid sterility.",\n            "clinical": "Open-label single-arm or randomized trials in high-unmet-need patients; mandatory long-term follow-up (up to 15 years) for gene-integration safety.",\n            "regulatory": "FDA CBER BLA under PHS Act § 351(a); RMAT (Regenerative Medicine Advanced Therapy) designation and strict comparability (ICH Q5E).",\n            "manufacturing": "Autologous patient-specific vein-to-vein cell processing (apheresis -> transduction -> expansion -> cryopreservation) or suspension HEK293 AAV bioreactor + TFF.",\n            "commercial": "One-time curative pricing models, outcomes-based payer contracts, Medicaid/CMS Cell & Gene Therapy Access Model, and hospital DRG reimbursement.",\n            "distribution": "Cryogenic liquid-nitrogen (LN2, <-150°C) specialty couriers (e.g., Cryoport/Marken) with strict Chain of Identity (COI) and REMS-certified treatment centers.",\n        },\n        "key_equipment": ["eq-single-use-bioreactor", "eq-tff-skid", "eq-sterile-fill-finish"],\n        "sources": [\n            "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research",\n            "https://www.fda.gov/patients/drug-development-process/step-5-fda-post-market-drug-safety-monitoring",\n        ],\n    },\n]\n\n\ndef build_playbooks(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    out_path = data_dir / "playbooks.json"\n    payload = {\n        "checked": CHECKED,\n        "count": len(PLAYBOOKS),\n        "stages": [{"id": s[0], "label": s[1]} for s in STAGES],\n        "modalities": PLAYBOOKS,\n    }\n    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {"modality_playbooks": len(PLAYBOOKS), "stages_compared": len(STAGES)}\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_playbooks(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
PLAYBOOKS_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nexport async function playbooksPage(query) {\n  const doc = await getJSON("data/playbooks.json");\n  const mods = doc.modalities || [];\n  const stages = doc.stages || [];\n  const selected = (query && query.get("stage")) || "";\n  const shownStages = selected ? stages.filter((s) => s.id === selected) : stages;\n\n  return {\n    title: "Modality Playbooks — Small Molecule vs. mAb vs. Peptide vs. Oligo vs. CGT",\n    body: html`\n      <h1>Modality Playbooks: End-to-End Comparison</h1>\n      <p class="lead">Developing an oral small-molecule pill is fundamentally different from manufacturing a monoclonal antibody, an LNP-delivered siRNA, or an autologous CAR-T cell therapy. Compare all 5 major modalities across all 8 lifecycle stages (checked ${doc.checked}).</p>\n      <p class="small">Focus on a single stage:\n        <a href="#/ref/playbooks">All 8 Stages</a>\n        ${stages.map((s) => html` · <a href="#/ref/playbooks?stage=${s.id}">${s.label}</a>`)}\n      </p>\n      <div class="tbl-wrap" tabindex="0" role="region" aria-label="Modality comparison matrix across 8 lifecycle stages">\n        <table class="tbl">\n          <thead>\n            <tr>\n              <th>Lifecycle Stage</th>\n              ${mods.map((m) => html`<th>${m.name}<br><span class="muted small">${m.mw_range}</span></th>`)}\n            </tr>\n          </thead>\n          <tbody>\n            ${shownStages.map((st) => html`\n              <tr>\n                <td><b><a href="#/ref/departments/${st.id}">${st.label}</a></b></td>\n                ${mods.map((m) => html`<td>${(m.stages || {})[st.id] || "—"}</td>`)}\n              </tr>\n            `)}\n            <tr>\n              <td><b>Browse Catalogue</b></td>\n              ${mods.map((m) => html`<td><a href="${m.catalogue_filter}">View medicines &rarr;</a></td>`)}\n            </tr>\n          </tbody>\n        </table>\n      </div>\n      <p class="muted small">Cross-links: <a href="#/ref/departments">8-Stage Lifecycle</a> · <a href="#/ref/equipment">18 Hardware Classes</a> · <a href="#/ref/software">10 Software Systems</a> · <a href="#/ref/partners">Partner Ecosystem</a>.</p>\n    `,\n  };\n}\n\nexport async function playbooksExplorePage() {\n  const doc = await getJSON("data/playbooks.json");\n  const mods = doc.modalities || [];\n  return {\n    title: "5 Types of Modern Medicines & How They Are Built",\n    body: html`\n      <h1>5 Types of Modern Medicines &amp; How They Are Built</h1>\n      <p class="lead">Not every medicine is a chemical pill pressed in a factory. Today\'s medicines range from tiny synthetic molecules to giant proteins, genetic RNA strands, and living engineered cells.</p>\n      <ol>${mods.map((m) => html`<li>\n        <b>${m.name}</b> <span class="muted">(${m.mw_range})</span>: ${m.plain_summary}\n        <br><span class="muted small"><b>How it reaches patients:</b> ${(m.stages || {}).distribution}</span>\n      </li>`)}</ol>\n      <p class="muted small"><a href="#/ref/playbooks">Open full 8-stage Reference comparison matrix</a> · <a href="#/explore/how-drugs-are-built">Back to 8-Stage Lifecycle</a>.</p>\n    `,\n  };\n}\n'
V60_QUIZ_EXTRA = [{'q': 'Under FDA regulations (21 CFR Part 312), how long does the FDA have to review an initial Investigational New Drug (IND) application before a sponsor may begin Phase 1 human clinical trials?', 'choices': ['30 calendar days', '6 months', '180 business days', '1 year'], 'answer': 0, 'explain': 'Under 21 CFR 312.40, an IND goes into effect 30 days after the FDA receives it unless the agency notifies the sponsor of a clinical hold.', 'source': 'eCFR — 21 CFR Part 312', 'url': 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312'}, {'q': 'Which federal regulation governs electronic records and electronic signatures in pharmaceutical ELN, LIMS, EDC, and MES software systems?', 'choices': ['21 CFR Part 11', '21 CFR Part 206', '21 CFR Part 58', '21 CFR Part 202'], 'answer': 0, 'explain': '21 CFR Part 11 sets the criteria under which FDA considers electronic records, electronic signatures, and audit trails to be trustworthy and equivalent to paper records.', 'source': 'eCFR — 21 CFR Part 11', 'url': 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11'}, {'q': 'In the Congressional Budget Office (CBO, 2021) review of pharmaceutical R&D, what was the reported capitalized R&D cost range per new approved drug across published studies?', 'choices': ['Under $1 billion to over $2 billion', '$50 million to $150 million', '$200 million to $400 million', '$10 billion to $15 billion'], 'answer': 0, 'explain': 'CBO (2021) reported estimates ranging from less than $1 billion to more than $2 billion per new approved drug once clinical trial failures and the time cost of capital are included.', 'source': 'CBO (2021) — Research and Development in the Pharmaceutical Industry', 'url': 'https://www.cbo.gov/publication/57025'}, {'q': 'Which federal law requires interoperable, unit-level electronic serialization (2D DataMatrix barcodes) across U.S. pharmaceutical manufacturers, 3PLs, wholesalers, and pharmacies?', 'choices': ['Drug Supply Chain Security Act (DSCSA)', 'Hatch-Waxman Act of 1984', 'Orphan Drug Act of 1983', 'Durham-Humphrey Amendment of 1951'], 'answer': 0, 'explain': 'The Drug Supply Chain Security Act (DSCSA) establishes electronic product tracing and unit-level serialization to prevent counterfeit or diverted prescription drugs from entering the U.S. supply chain.', 'source': 'FDA — Drug Supply Chain Security Act (DSCSA)', 'url': 'https://www.fda.gov/media/77516/download'}, {'q': 'Which FDA regulation governs Good Laboratory Practice (GLP) for nonclinical animal toxicology studies required before an IND filing?', 'choices': ['21 CFR Part 58', '21 CFR Part 211', '21 CFR Part 314', '21 CFR Part 11'], 'answer': 0, 'explain': '21 CFR Part 58 sets Good Laboratory Practice (GLP) standards for nonclinical laboratory studies that support research or marketing permits for FDA-regulated products.', 'source': 'eCFR — 21 CFR Part 58', 'url': 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-58'}, {'q': "Under FDA's regulatory boundary for synthetic peptides vs. biologics, how is a chemically synthesized peptide of 40 or fewer amino acids regulated?", 'choices': ['As a drug under an NDA (FD&C Act)', 'As a biologic under a BLA (PHS Act § 351)', 'As a medical device under a 510(k)', 'As an OTC monograph product'], 'answer': 0, 'explain': 'FDA regulates amino acid polymers of 40 or fewer amino acids as drugs (NDA pathway under 21 CFR Part 314), whereas polymers exceeding 40 amino acids are regulated as biological products (BLA pathway).', 'source': 'eCFR — 21 CFR Part 314', 'url': 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314'}, {'q': 'Which type of execution partner can legally assume transferred clinical trial obligations from a drug sponsor under 21 CFR 312.52?', 'choices': ['Contract Research Organization (CRO)', 'Full-Line Pharmaceutical Wholesaler', 'Pharmacy Benefit Manager (PBM)', 'Health Technology Assessment (HTA) body'], 'answer': 0, 'explain': 'Under 21 CFR 312.52, a sponsor may transfer responsibility for any or all clinical trial obligations to a Contract Research Organization (CRO) in writing.', 'source': 'eCFR — 21 CFR Part 312', 'url': 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312'}, {'q': 'In commercial U.S. drug pricing, what is the published list price set by a manufacturer before wholesaler fees, PBM rebates, and statutory 340B/Medicaid discounts are deducted?', 'choices': ['Wholesale Acquisition Cost (WAC)', 'Average Sales Price (ASP)', 'Maximum Fair Price (MFP)', 'Incremental Cost-Effectiveness Ratio (ICER)'], 'answer': 0, 'explain': "Wholesale Acquisition Cost (WAC) is the manufacturer's published list price to wholesalers before commercial PBM rebates, 340B discounts, Medicaid Best Price, or Medicare negotiations.", 'source': 'CMS — Medicare Drug Price Negotiation Program', 'url': 'https://www.cms.gov/initiatives/medicare-prescription-drug-affordability/overview/medicare-drug-price-negotiation-program'}]


def _patch_app_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    imp = 'import { playbooksPage, playbooksExplorePage } from "./playbooks.js";\n'
    if "./playbooks.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/playbooks"' not in txt:
        for anchor in ('if (path === "/ref/partners")', 'if (path === "/ref/software")', 'if (path === "/ref/equipment")'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/playbooks") return playbooksPage(query);\n'
                    '  if (path === "/explore/playbooks") return playbooksExplorePage();\n'
                    '  ' + anchor
                )
                txt = txt.replace(anchor, rep, 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_layout_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "#/ref/playbooks" in txt:
        return False
    for anchor in ('["#/ref/partners", "Partner ecosystem"]', '["#/ref/economics", "Drug economics"]', '["#/ref/equipment", "Equipment market"]'):
        if anchor in txt:
            rep = anchor + ',\n  ["#/ref/playbooks", "Modality playbooks"]'
            path.write_text(txt.replace(anchor, rep, 1), encoding="utf-8")
            return True
    return False


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_playbooks.py" in txt:
        return False
    hook = "\n# v6.0l: Modality Playbooks (5 Modalities x 8 Lifecycle Stages)\npython3 pipeline/build_playbooks.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/playbooks"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/playbooks")\n'
        'def api_playbooks():\n'
        '    return _read_json(SITE_DIR / "data" / "playbooks.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_quiz_extra(path: pathlib.Path) -> int:
    if path.is_file():
        data = json.loads(path.read_text(encoding="utf-8"))
        items = data.get("questions") if isinstance(data, dict) else data
    else:
        data = []
        items = data
    if not isinstance(items, list):
        raise ValueError(f"Unexpected quiz_extra.json format in {path}")
    existing = {str(x.get("q", "")).strip() for x in items}
    added = 0
    for q in V60_QUIZ_EXTRA:
        if q["q"].strip() not in existing:
            items.append(q)
            existing.add(q["q"].strip())
            added += 1
    if added or not path.is_file():
        if isinstance(data, dict):
            data["questions"] = items
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        else:
            path.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return added


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    pipe_dir.mkdir(parents=True, exist_ok=True)
    js_dir.mkdir(parents=True, exist_ok=True)

    fp_py = pipe_dir / "build_playbooks.py"
    py_written = (not fp_py.is_file()) or (fp_py.read_text(encoding="utf-8") != BUILD_PLAYBOOKS_PY)
    if py_written:
        fp_py.write_text(BUILD_PLAYBOOKS_PY, encoding="utf-8")

    fp_js = js_dir / "playbooks.js"
    js_written = (not fp_js.is_file()) or (fp_js.read_text(encoding="utf-8") != PLAYBOOKS_JS)
    if js_written:
        fp_js.write_text(PLAYBOOKS_JS, encoding="utf-8")

    return {
        "build_playbooks_py": py_written,
        "playbooks_js": js_written,
        "app_js_wired": _patch_app_js(js_dir / "app.js"),
        "layout_js_wired": _patch_layout_js(js_dir / "layout.js"),
        "run_all_sh_hooked": _patch_run_all(pipe_dir / "run_all.sh"),
        "app_py_api_added": _patch_app_py(root / "app.py"),
        "quiz_questions_added": _patch_quiz_extra(pipe_dir / "quiz_extra.json"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        (root / "site" / "data").mkdir(parents=True)

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/partners") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV = [\n  ["#/ref/partners", "Partner ecosystem"],\n];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "quiz_extra.json").write_text("[]\n", encoding="utf-8")

        r1 = apply_patch(root)
        assert r1["quiz_questions_added"] == 8 and all(v for k, v in r1.items() if k != "quiz_questions_added"), r1
        r2 = apply_patch(root)
        assert r2["quiz_questions_added"] == 0 and not any(v for k, v in r2.items() if k != "quiz_questions_added"), r2

        py_compile.compile(str(root / "pipeline" / "build_playbooks.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_playbooks.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out["modality_playbooks"] == 5 and out["stages_compared"] == 8, out

        doc = json.loads((root / "site" / "data" / "playbooks.json").read_text(encoding="utf-8"))
        for m in doc["modalities"]:
            assert len(m["stages"]) == 8 and all(u.startswith("https://") for u in m["sources"]), m
        qdoc = json.loads((root / "pipeline" / "quiz_extra.json").read_text(encoding="utf-8"))
        assert len(qdoc) == 8 and all(q["url"].startswith("https://") for q in qdoc), qdoc

        print("V60L_PLAYBOOKS_AND_QUIZ_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.0l Modality Playbooks & v6.0 Quiz patch.")
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
