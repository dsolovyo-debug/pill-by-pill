#!/usr/bin/env python3
"""Pill by Pill v6.1j Patch: Pharmaceutical Chemistry, ADME/PK, BCS & Drug Delivery Reference (#/ref/adme, #/explore/adme, /api/adme).

1. Adds `pipeline/build_adme.py` -> `site/data/adme.json` (4 ADME pillars, 6 PK parameters,
   4 ICH M9 BCS classes, 5 MedChem drug-likeness rules, 5 DDI/special-population frameworks,
   and 6 advanced drug-delivery technologies — 30 primary-sourced entries total).
2. Adds `site/js/adme.js` (`admePage` with inline ADME flow SVG + 6 section jump filters) and
   wires `#/ref/adme`, `#/explore/adme`, `/api/adme`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `adme.json` into `pipeline/build_global_search.py`, `pipeline/build_v60_static_pages.py`
   (`/adme/` static SEO page + sitemap entry -> 26 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1j_adme_pk_medchem_and_delivery_patch.py --selftest
  python3 2026-11-23_v6.1j_adme_pk_medchem_and_delivery_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_ADME_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1j Pharmaceutical Chemistry, ADME/PK & Drug Delivery dataset (`site/data/adme.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. ADME Pillars (Absorption, Distribution, Metabolism, Excretion)\n  2. Core Pharmacokinetic (PK) Parameters & Dosing Concepts (6)\n  3. Biopharmaceutics Classification System — BCS Classes I–IV (4, ICH M9)\n  4. Medicinal Chemistry & Drug-Likeness Rules (5: Lipinski Ro5, Veber, bRo5, CNS/BBB, Reactive Alerts)\n  5. Drug-Drug Interactions (DDIs) & Special Populations (5: CYP Inhibition, Induction, Transporters, Organ Impairment, PGx)\n  6. Advanced Drug Delivery & Formulation Engineering (6: Modified Release, ASDs, LNPs, ADCs, LAIs, Oral Peptides)\n\nAll regulatory & scientific anchors are verified HTTPS primary sources (FDA, eCFR, ICH, NIH/PMC).\n\nUsage:\n  python3 pipeline/build_adme.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-23"\n\nADME_PILLARS = [\n    {\n        "id": "adme-absorption",\n        "name": "A — Absorption & Bioavailability (F)",\n        "plain": "How a medicine travels from where you take it (such as your stomach, skin, or muscle) into your bloodstream—and how much actually survives the first trip through the liver.",\n        "technical": "Governed by dissolution rate, GI pH/ionization (Henderson-Hasselbalch), passive transcellular permeability, active uptake/efflux transporters (P-gp, BCRP), and intestinal/hepatic first-pass metabolism (CYP3A4). Oral bioavailability F = Fa × Fg × Fh.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/m9-biopharmaceutics-classification-system-based-biowaivers",\n    },\n    {\n        "id": "adme-distribution",\n        "name": "D — Distribution & Tissue Targeting",\n        "plain": "Once in the blood, how widely the medicine spreads into organs, fat, or the brain—and how tightly it rides on blood proteins like albumin.",\n        "technical": "Quantified by apparent Volume of Distribution (Vd). Influenced by plasma protein binding (albumin, alpha-1-acid glycoprotein), tissue affinity, perfusion rate, and physiological barriers such as the Blood-Brain Barrier (BBB) tight junctions and P-gp efflux.",\n        "url": "https://www.fda.gov/patients/drug-development-process/step-2-preclinical-research",\n    },\n    {\n        "id": "adme-metabolism",\n        "name": "M — Metabolism (Biotransformation)",\n        "plain": "How liver enzymes chemically remodel a drug—usually turning fat-soluble molecules into water-soluble ones that are easier to flush out, or switching an inactive \'prodrug\' into its active form.",\n        "technical": "Phase I functionalization (cytochrome P450 superfamily — CYP3A4, 2D6, 2C9, 2C19, 1A2 — plus esterases/FMOs) and Phase II conjugation (UGT glucuronidation, SULT sulfation, NAT acetylation, GST). Determines prodrug activation (e.g., clopidogrel, codeine) and active/reactive metabolite risk (FDA MIST guidance).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-testing-drug-metabolites",\n    },\n    {\n        "id": "adme-excretion",\n        "name": "E — Excretion & Elimination",\n        "plain": "How the body finally clears the medicine and its breakdown products—mostly through the kidneys into urine or through the liver and bile into stool.",\n        "technical": "Renal elimination combines glomerular filtration (unbound fraction × GFR), active proximal-tubular secretion (OAT1/3, OCT2, MATE1/2-K), and passive tubular reabsorption. Hepatic/biliary excretion involves MRP2/BCRP and can undergo enterohepatic recirculation.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pharmacokinetics-patients-impaired-renal-function-study-design-data-analysis-and-impact-dosing",\n    },\n]\n\nPK_PARAMETERS = [\n    {\n        "id": "pk-half-life",\n        "name": "Elimination Half-Life (t½) & Steady State",\n        "symbol": "t½ = 0.693 × Vd / CL",\n        "plain": "The time it takes for the amount of medicine in your blood to drop by half. Taking regular doses reaches a steady, balanced level after about 4 to 5 half-lives.",\n        "technical": "Dependent secondary parameter driven by both Clearance (CL) and Volume of Distribution (Vd). Dictates dosing interval, time to steady state (~94–97% at 4–5 half-lives), washout duration in crossover trials, and whether a loading dose is needed.",\n        "url": "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research",\n    },\n    {\n        "id": "pk-clearance",\n        "name": "Systemic Clearance (CL)",\n        "symbol": "CL = Dose × F / AUC",\n        "plain": "The volume of blood completely cleaned of the medicine per minute or hour—determining what daily maintenance dose is needed to keep the drug at its target level.",\n        "technical": "Primary PK parameter (units: L/h or mL/min) representing the sum of hepatic, renal, and other organ clearances (CLtotal = CLh + CLr + CLother). Maintenance dose rate at steady state equals CL × Css,avg / F.",\n        "url": "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research",\n    },\n    {\n        "id": "pk-vd",\n        "name": "Volume of Distribution (Vd)",\n        "symbol": "Vd = Amount in body / Cplasma",\n        "plain": "A measure of whether a medicine stays mostly inside the bloodstream (small Vd, like large antibodies) or spreads deeply into muscles and body tissues (large Vd).",\n        "technical": "Apparent proportionality constant linking plasma concentration to total drug amount in the body. Monoclonal antibodies typically exhibit Vd ≈ 3–8 L (vascular/interstitial space), whereas lipophilic basic small molecules can exceed 1,000 L due to extensive tissue partitioning.",\n        "url": "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research",\n    },\n    {\n        "id": "pk-exposure",\n        "name": "Cmax, Tmax & Area Under the Curve (AUC)",\n        "symbol": "AUC0–∞, Cmax, Tmax",\n        "plain": "Cmax is the highest peak level in the blood, Tmax is how fast it gets there, and AUC is the total exposure over time—the three numbers regulators check to prove generic pills match brand-name drugs.",\n        "technical": "Core non-compartmental analysis (NCA) exposure metrics. Peak concentration (Cmax) often correlates with acute toxicity or rapid onset; AUC reflects total systemic exposure and anchors FDA bioequivalence (80–125% 90% CI).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/bioavailability-studies-submitted-ndas-or-inds-general-considerations",\n    },\n    {\n        "id": "pk-bioavailability",\n        "name": "Absolute & Relative Bioavailability (F)",\n        "symbol": "F = (AUCoral / Doseoral) / (AUCiv / Doseiv)",\n        "plain": "The percentage of a swallowed pill that actually reaches the bloodstream intact compared to injecting it directly into a vein (which is 100%).",\n        "technical": "Low oral F can stem from poor solubility/dissolution, gut-wall degradation, efflux transport, or high hepatic extraction ratio. Food effects can raise F (lipophilic drugs with high-fat meals) or lower F (chelation or gastric-emptying delay).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/bioavailability-studies-submitted-ndas-or-inds-general-considerations",\n    },\n    {\n        "id": "pk-nti",\n        "name": "Therapeutic Window & Narrow Therapeutic Index (NTI)",\n        "symbol": "MEC ↔ MTC",\n        "plain": "The safe \'Goldilocks zone\' between too little drug (doesn\'t work) and too much drug (causes side effects). NTI drugs like warfarin or levothyroxine have a razor-thin safety margin.",\n        "technical": "Span between Minimum Effective Concentration (MEC) and Minimum Toxic Concentration (MTC). NTI drugs (warfarin, lithium, levothyroxine, tacrolimus, phenytoin) require tighter FDA reference-scaled bioequivalence limits and often therapeutic drug monitoring (TDM).",\n        "url": "https://www.fda.gov/drugs/guidance-compliance-regulatory-information/guidances-drugs",\n    },\n]\n\nBCS_CLASSES = [\n    {\n        "id": "bcs-1",\n        "name": "BCS Class I — High Solubility, High Permeability",\n        "plain": "Dissolves quickly in stomach fluid and crosses the gut wall easily—the easiest type of medicine to turn into a reliable oral pill.",\n        "technical": "Dissolves completely across pH 1.2–6.8 in <=250 mL aqueous media and shows >=85% human absorption (ICH M9). Gastric emptying is typically rate-limiting; eligible for FDA/EMA/ICH M9 BCS-based biowaivers for immediate-release oral solids.",\n        "strategy": "Standard immediate-release tablets/capsules; straightforward generic bioequivalence.",\n        "examples": "Metoprolol, propranolol, acetaminophen, levofloxacin.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/m9-biopharmaceutics-classification-system-based-biowaivers",\n    },\n    {\n        "id": "bcs-2",\n        "name": "BCS Class II — Low Solubility, High Permeability",\n        "plain": "Crosses the gut wall easily once dissolved, but behaves like \'brick dust\' in water—so formulation scientists must engineer special powders or coatings to help it dissolve.",\n        "technical": "Dissolution-rate limited absorption; represents a large share of modern small-molecule discovery pipelines due to lipophilic target binding pockets. Often exhibits strong positive food effects.",\n        "strategy": "Amorphous Solid Dispersions (ASDs via spray drying or hot-melt extrusion), particle-size reduction/nanomilling, salt forms, lipid/self-emulsifying systems (SEDDS).",\n        "examples": "Ibuprofen, atorvastatin, carbamazepine, venetoclax, ivacaftor.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/m9-biopharmaceutics-classification-system-based-biowaivers",\n    },\n    {\n        "id": "bcs-3",\n        "name": "BCS Class III — High Solubility, Low Permeability",\n        "plain": "Dissolves easily in water, but struggles to squeeze across the fatty cell membranes lining the intestine.",\n        "technical": "Permeability-rate limited absorption; sensitive to GI transit time and excipients that alter motility or tight junctions. Eligible for ICH M9 biowaivers only with very rapid dissolution (>=85% in 15 min) and qualitatively identical / quantitatively very similar excipients.",\n        "strategy": "Prodrug esterification to boost lipophilicity, permeation enhancers, or parenteral delivery if oral absorption is insufficient.",\n        "examples": "Metformin, acyclovir, atenolol, cimetidine.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/m9-biopharmaceutics-classification-system-based-biowaivers",\n    },\n    {\n        "id": "bcs-4",\n        "name": "BCS Class IV — Low Solubility, Low Permeability",\n        "plain": "The toughest oral formulation challenge: neither dissolves well in water nor crosses the gut lining easily.",\n        "technical": "Poor and highly variable oral bioavailability; frequently subject to P-gp efflux and intestinal metabolism. Not eligible for BCS-based biowaivers.",\n        "strategy": "Enabling amorphous/lipid formulations, prodrug redesign in medicinal chemistry, or switching to intravenous/subcutaneous parenteral routes.",\n        "examples": "Furosemide, paclitaxel (IV), amphotericin B (IV liposomal).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/m9-biopharmaceutics-classification-system-based-biowaivers",\n    },\n]\n\nMEDCHEM_RULES = [\n    {\n        "id": "mc-lipinski",\n        "name": "Lipinski\'s Rule of 5 (Oral Small-Molecule Drug-Likeness)",\n        "plain": "A famous 1997 rule of thumb: oral pills are much more likely to absorb well if they stay relatively small (MW <= 500), not too greasy (LogP <= 5), and without too many sticky hydrogen-bond groups.",\n        "technical": "Poor absorption/permeation is more likely when >1 of the following occurs: Molecular Weight > 500 Da, cLogP > 5, Hydrogen-Bond Donors (HBD) > 5, or Hydrogen-Bond Acceptors (HBA) > 10. Directly surfaced on Pill by Pill Reference drug cards.",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3117226/",\n    },\n    {\n        "id": "mc-veber",\n        "name": "Veber\'s Rules (Molecular Flexibility & Polar Surface Area)",\n        "plain": "Even if a molecule is small, being too \'floppy\' or too electrically polar makes it hard to slip through cell membranes into the bloodstream.",\n        "technical": "Predicts good oral bioavailability in rats independent of MW when Rotatable Bonds <= 10 AND Topological Polar Surface Area (TPSA) <= 140 Å² (or <= 12 total H-bond donors + acceptors).",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3117226/",\n    },\n    {\n        "id": "mc-bro5",\n        "name": "Beyond Rule of 5 (bRo5) Chemical Space",\n        "plain": "Modern drugs targeting flat, hard-to-hit proteins—like venetoclax, hepatitis C antivirals, macrocycles, and PROTAC degraders—break Lipinski\'s size limits by folding inward to hide polar groups.",\n        "technical": "Molecules with MW 500–1,200+ Da (e.g., venetoclax, cyclosporine, macrolides, heterobifunctional PROTACs) achieve oral bioavailability via intramolecular hydrogen bonding (\'chameleonicity\') and advanced ASD formulations.",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8895297/",\n    },\n    {\n        "id": "mc-cns-bbb",\n        "name": "Blood-Brain Barrier (BBB) & CNS Drug Design",\n        "plain": "Brain medicines face an extra security wall: the blood-brain barrier blocks large or polar molecules and actively pumps intruders back out.",\n        "technical": "CNS Multiparameter Optimization (CNS MPO) favors tighter limits: MW < 400–450 Da, TPSA < 60–90 Å², HBD <= 1–2, moderate LogD (1–3), and low P-gp/BCRP efflux ratio (Kp,uu optimization).",\n        "url": "https://www.fda.gov/patients/drug-development-process/step-1-discovery-and-development",\n    },\n    {\n        "id": "mc-alerts",\n        "name": "Structural Alerts, Reactive Metabolites & hERG/Safety Screening",\n        "plain": "Chemists screen out \'troublemaker\' chemical groups early so a drug does not damage the liver, mutate DNA, or disrupt heart rhythms.",\n        "technical": "Early triage flags genotoxic/mutagenic alerts (ICH M7 / Ames assay), covalent reactive metabolites linked to idiosyncratic DILI, hERG K+ channel blockade (QT prolongation, ICH S7B), and Pan-Assay Interference Compounds (PAINS).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/m7r2-assessment-and-control-dna-reactive-mutagenic-impurities-pharmaceuticals-limit-potential",\n    },\n]\n\nDDIS_AND_POPS = [\n    {\n        "id": "ddi-cyp-inh",\n        "name": "CYP450 Enzyme Inhibition (Reversible & Time-Dependent)",\n        "plain": "When one medicine (or grapefruit juice) slows down a liver enzyme, a second medicine processed by that same enzyme builds up to potentially toxic levels.",\n        "technical": "FDA Clinical DDI Guidance classifies strong (>=5-fold AUC increase), moderate (2–5-fold), and weak (1.25–2-fold) CYP inhibitors (e.g., ritonavir/clarithromycin on CYP3A4). Time-dependent / mechanism-based inhibition (MBI) persists until new enzyme is synthesized.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-drug-interaction-studies-cytochrome-p450-enzyme-and-transporter-mediated-drug-interactions",\n    },\n    {\n        "id": "ddi-cyp-ind",\n        "name": "CYP450 Enzyme Induction (PXR / CAR)",\n        "plain": "Some medicines and herbs (like rifampin or St. John\'s wort) tell liver cells to build extra breakdown enzymes—causing other drugs to clear too fast and stop working.",\n        "technical": "Nuclear receptor activation (PXR, CAR, AhR) upregulates CYP3A4, CYP2C9, UGTs, and P-gp transcription over days to weeks; strong inducers (rifampin, carbamazepine, phenytoin) can reduce victim drug AUC by >80%.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-drug-interaction-studies-cytochrome-p450-enzyme-and-transporter-mediated-drug-interactions",\n    },\n    {\n        "id": "ddi-transporters",\n        "name": "Membrane Transporters (P-gp, BCRP, OATP1B1/1B3, OAT/OCT)",\n        "plain": "Molecular \'pumps and gates\' on gut, liver, and kidney cells actively pull drugs in or push them out—blocking them can sharply change drug levels in blood or muscle.",\n        "technical": "FDA In Vitro DDI Guidance mandates evaluation of efflux (P-gp, BCRP) and uptake (OATP1B1/1B3 for statins, OAT1/3, OCT2, MATE1/2-K) transporters as both substrates and inhibitors.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/in-vitro-drug-interaction-studies-cytochrome-p450-enzyme-and-transporter-mediated-drug-interactions",\n    },\n    {\n        "id": "ddi-organ",\n        "name": "Renal & Hepatic Impairment Dosing Adjustments",\n        "plain": "If a patient\'s kidneys or liver are weakened, medicines cleared by those organs stay in the body longer and require lower or less frequent doses.",\n        "technical": "Dedicated FDA renal impairment studies (stratified by eGFR/CrCl) and hepatic impairment studies (Child-Pugh Classes A, B, C) establish label-specific dose reductions or contraindications.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pharmacokinetics-patients-impaired-renal-function-study-design-data-analysis-and-impact-dosing",\n    },\n    {\n        "id": "ddi-pgx",\n        "name": "Pharmacogenomics (Genetic Polymorphisms in Metabolism)",\n        "plain": "Natural DNA differences in liver enzymes mean one person may break down a drug super fast while another barely processes it at all—changing both safety and effectiveness.",\n        "technical": "Key actionable genes in FDA labeling and CPIC guidelines: CYP2C19 (clopidogrel prodrug activation), CYP2D6 (codeine/tamoxifen), CYP2C9/VKORC1 (warfarin), TPMT/NUDT15 (thiopurines), and DPYD (5-fluorouracil toxicity).",\n        "url": "https://www.fda.gov/drugs/science-and-research-drugs/table-pharmacogenomic-biomarkers-drug-labeling",\n    },\n]\n\nDELIVERY_TECH = [\n    {\n        "id": "del-modified-release",\n        "name": "Modified-Release Oral Systems (ER, DR & Osmotic OROS)",\n        "plain": "Special polymer coatings and microscopic laser-drilled pumps that release a medicine steadily over 12–24 hours or wait until a pill passes stomach acid.",\n        "technical": "Includes enteric delayed-release (pH-responsive methacrylic polymers protecting acid-labile PPIs), hydrophilic HPMC matrix tablets, and zero-order osmotic pumps (OROS); must pass alcohol dose-dumping and dissolution testing.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q8r2-pharmaceutical-development",\n    },\n    {\n        "id": "del-asd",\n        "name": "Amorphous Solid Dispersions (ASDs — Spray Drying & HME)",\n        "plain": "Locks a hard-to-dissolve drug into a disordered \'glassy\' polymer matrix so it dissolves many times faster in the gut than rigid crystals.",\n        "technical": "Manufactured via Spray Drying (using eq-spray-dryer) or Hot-Melt Extrusion (HME) to generate supersaturated luminal concentrations for BCS Class II/IV APIs while inhibiting recrystallization during shelf life.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q8r2-pharmaceutical-development",\n    },\n    {\n        "id": "del-lnp",\n        "name": "Lipid Nanoparticles (LNPs) & GalNAc Conjugates",\n        "plain": "Protective microscopic fat bubbles (LNPs) or liver-homing sugar tags (GalNAc) that escort fragile siRNA and mRNA strands safely inside target cells.",\n        "technical": "Four-lipid LNP architecture (ionizable lipid pKa ~6.2–6.5 for endosomal escape, DSPC, cholesterol, PEG-lipid) assembled by microfluidic mixing (eq-microfluidic-lnp), or trivalent GalNAc targeting hepatocyte ASGPR.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/liposome-drug-products-chemistry-manufacturing-and-controls-human-pharmacokinetics-and-bioavailability",\n    },\n    {\n        "id": "del-adc",\n        "name": "Antibody-Drug Conjugates (ADCs — Guided Payloads)",\n        "plain": "Attaches a potent chemotherapy payload onto a targeting antibody via a chemical linker so the toxic drug is released primarily inside tumor cells.",\n        "technical": "Engineered across 3 critical attributes: target-specific mAb, Drug-to-Antibody Ratio (DAR) homogeneity, and cleavable vs. non-cleavable linker stability controlling systemic release and bystander killing.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-pharmacology-considerations-antibody-drug-conjugates",\n    },\n    {\n        "id": "del-lai",\n        "name": "Long-Acting Injectables (LAIs & Biodegradable Depots)",\n        "plain": "Slow-dissolving muscle or under-the-skin injections that release medicine steadily for a month, three months, or even six months from a single shot.",\n        "technical": "Utilizes biodegradable PLGA microspheres, nanocrystal aqueous suspensions, or in situ forming polymer depots exhibiting \'flip-flop\' pharmacokinetics (absorption rate slower than elimination rate).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q8r2-pharmaceutical-development",\n    },\n    {\n        "id": "del-oral-peptide",\n        "name": "Oral Peptide & Biologic Permeation Enhancers",\n        "plain": "Clever tablet chemistry (like SNAC in oral semaglutide) that shields fragile peptides from stomach acid and temporarily opens a local path across the stomach lining.",\n        "technical": "Co-formulation with absorption enhancers (e.g., salcaprozate sodium / SNAC) creates a localized pH-buffered microenvironment inhibiting pepsin degradation and enhancing transcellular monomer permeation.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q8r2-pharmaceutical-development",\n    },\n]\n\n\ndef build_adme(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced reference on ADME/PK, Biopharmaceutics (BCS), Medicinal Chemistry drug-likeness, DDIs, and drug delivery engineering (FDA, ICH, NIH/PMC). Educational reference only.",\n        "adme_pillars": ADME_PILLARS,\n        "pk_parameters": PK_PARAMETERS,\n        "bcs_classes": BCS_CLASSES,\n        "medchem_rules": MEDCHEM_RULES,\n        "ddis_and_pops": DDIS_AND_POPS,\n        "delivery_tech": DELIVERY_TECH,\n    }\n    (data_dir / "adme.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "adme_pillars": len(ADME_PILLARS),\n        "pk_parameters": len(PK_PARAMETERS),\n        "bcs_classes": len(BCS_CLASSES),\n        "medchem_rules": len(MEDCHEM_RULES),\n        "ddis_and_pops": len(DDIS_AND_POPS),\n        "delivery_tech": len(DELIVERY_TECH),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_adme(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
ADME_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderAdmeFlowSvg() {\n  const nodes = [\n    { x: 10, label: "1. Absorption (A)", sub: "Gut / Route -> Blood" },\n    { x: 175, label: "2. Distribution (D)", sub: "Blood -> Target Tissue" },\n    { x: 340, label: "3. Metabolism (M)", sub: "Liver CYP450 / UGT" },\n    { x: 505, label: "4. Excretion (E)", sub: "Kidney / Bile Clearance" },\n  ];\n  return html`<figure class="adme-flow" aria-label="ADME pharmacokinetic journey inside the human body">\n    <svg viewBox="0 0 665 84" width="665" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="150" height="62" rx="9" fill="var(--paper,#f8fafc)" stroke="${i === 1 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 1 ? "2" : "1.5"}"/>\n        <text x="${n.x + 75}" y="35" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 75}" y="53" text-anchor="middle" font-size="10.5" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 150}" y1="41" x2="${n.x + 165}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">ADME journey: what the body does to a medicine (Pharmacokinetics) determines whether enough active drug reaches its target safely.</figcaption>\n  </figure>`;\n}\n\nexport async function admePage(query, mode = "ref") {\n  const doc = await getJSON("data/adme.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/adme" : "#/ref/adme";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "ADME/PK, Medicinal Chemistry, BCS & Drug Delivery Reference",\n    body: html`\n      <h1>Pharmaceutical Chemistry, ADME/PK &amp; Drug Delivery</h1>\n      <p class="lead">${mode === "explore"\n        ? "What happens to a medicine after you swallow a pill or receive an injection—how it dissolves, enters the blood, reaches its target, gets broken down by the liver, and leaves the body."\n        : "Primary-sourced reference covering ADME pillars, core PK equations, ICH M9 BCS Classes I–IV, Lipinski/Veber/bRo5 medicinal chemistry rules, CYP/transporter DDIs, and enabling drug-delivery systems (checked " + doc.checked + ")."}</p>\n\n      ${renderAdmeFlowSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=adme"${sec === "adme" ? \' aria-current="page"\' : ""}>ADME (4)</a> ·\n        <a href="${base}?section=pk"${sec === "pk" ? \' aria-current="page"\' : ""}>PK Math (6)</a> ·\n        <a href="${base}?section=bcs"${sec === "bcs" ? \' aria-current="page"\' : ""}>BCS I–IV (4)</a> ·\n        <a href="${base}?section=medchem"${sec === "medchem" ? \' aria-current="page"\' : ""}>MedChem Rules (5)</a> ·\n        <a href="${base}?section=ddis"${sec === "ddis" ? \' aria-current="page"\' : ""}>DDIs &amp; PGx (5)</a> ·\n        <a href="${base}?section=delivery"${sec === "delivery" ? \' aria-current="page"\' : ""}>Delivery Tech (6)</a>\n      </p>\n\n      ${show("adme") ? html`\n        <h2 id="adme">1. The Four ADME Pillars</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="ADME pillars">\n          <table class="tbl"><thead><tr><th>Pillar</th><th>${mode === "explore" ? "How It Works" : "Plain & Pharmacokinetic Mechanism"}</th></tr></thead>\n          <tbody>${(doc.adme_pillars || []).map((a) => html`<tr id="${a.id}">\n            <td><b><a href="${a.url}" target="_blank" rel="noopener">${a.name}</a></b></td>\n            <td>${mode === "explore" ? a.plain : html`${a.plain}<br><span class="muted small">${a.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("pk") ? html`\n        <h2 id="pk">2. Core Pharmacokinetic (PK) Parameters &amp; Dosing Math</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Core PK parameters">\n          <table class="tbl"><thead><tr><th>Parameter</th><th>Key Relation</th><th>${mode === "explore" ? "What It Tells Doctors" : "Clinical & Quantitative Meaning"}</th></tr></thead>\n          <tbody>${(doc.pk_parameters || []).map((p) => html`<tr id="${p.id}">\n            <td><b><a href="${p.url}" target="_blank" rel="noopener">${p.name}</a></b></td>\n            <td><code>${p.symbol}</code></td>\n            <td>${mode === "explore" ? p.plain : html`${p.plain}<br><span class="muted small">${p.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("bcs") ? html`\n        <h2 id="bcs">3. Biopharmaceutics Classification System (BCS Classes I–IV, ICH M9)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="BCS classes I to IV">\n          <table class="tbl"><thead><tr><th>BCS Class</th><th>Behavior &amp; Biowaiver Rules</th><th>Formulation Strategy &amp; Examples</th></tr></thead>\n          <tbody>${(doc.bcs_classes || []).map((b) => html`<tr id="${b.id}">\n            <td><b><a href="${b.url}" target="_blank" rel="noopener">${b.name}</a></b></td>\n            <td>${mode === "explore" ? b.plain : html`${b.plain}<br><span class="muted small">${b.technical}</span>`}</td>\n            <td><b>Strategy:</b> ${b.strategy}<br><span class="muted small"><b>Examples:</b> ${b.examples}</span></td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("medchem") ? html`\n        <h2 id="medchem">4. Medicinal Chemistry &amp; Drug-Likeness Guidelines</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Medicinal chemistry rules">\n          <table class="tbl"><thead><tr><th>Rule / Framework</th><th>${mode === "explore" ? "Why Chemists Use It" : "Criteria & Scope"}</th></tr></thead>\n          <tbody>${(doc.medchem_rules || []).map((m) => html`<tr id="${m.id}">\n            <td><b><a href="${m.url}" target="_blank" rel="noopener">${m.name}</a></b></td>\n            <td>${mode === "explore" ? m.plain : html`${m.plain}<br><span class="muted small">${m.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("ddis") ? html`\n        <h2 id="ddis">5. Drug-Drug Interactions (DDIs) &amp; Special Populations</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Drug-drug interactions and special populations">\n          <table class="tbl"><thead><tr><th>Mechanism / Population</th><th>Clinical &amp; Regulatory Impact</th></tr></thead>\n          <tbody>${(doc.ddis_and_pops || []).map((d) => html`<tr id="${d.id}">\n            <td><b><a href="${d.url}" target="_blank" rel="noopener">${d.name}</a></b></td>\n            <td>${mode === "explore" ? d.plain : html`${d.plain}<br><span class="muted small">${d.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("delivery") ? html`\n        <h2 id="delivery">6. Advanced Drug Delivery &amp; Formulation Engineering</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Advanced drug delivery technologies">\n          <table class="tbl"><thead><tr><th>Delivery Platform</th><th>How It Solves ADME/PK Bottlenecks</th></tr></thead>\n          <tbody>${(doc.delivery_tech || []).map((t) => html`<tr id="${t.id}">\n            <td><b><a href="${t.url}" target="_blank" rel="noopener">${t.name}</a></b></td>\n            <td>${mode === "explore" ? t.plain : html`${t.plain}<br><span class="muted small">${t.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/departments/formulation">Stage 2: Formulation</a> · <a href="#/ref/routes">Routes of Administration</a> · <a href="#/ref/equipment">18 Hardware Classes</a> · <a href="#/ref/trials">Clinical Trials &amp; Endpoints</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { admePage } from "./adme.js";\n'
    if "./adme.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/adme"' not in txt:
        for anchor in ('if (path === "/ref/trials")', 'if (path === "/ref/pathways")', 'if (path === "/ref/classes")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/adme") return admePage(query, "ref");\n'
                    '  if (path === "/explore/adme") return admePage(query, "explore");\n'
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
    changed = False
    if "#/ref/adme" not in txt:
        for anchor in ('["#/ref/trials", "Clinical trials & endpoints"]', '["#/ref/pathways", "Approval pathways"]', '["#/ref/ich", "ICH Q1–Q12 matrix"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/adme", "ADME/PK & MedChem"]', 1)
                changed = True
                break
    if "#/explore/adme" not in txt:
        for anchor in ('["#/explore/trials", "Clinical trials & endpoints"]', '["#/explore/pathways", "Approval pathways"]', '["#/explore/worksheets", "Teacher worksheets"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/adme", "ADME & how pills work"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_adme.py" in txt:
        return False
    hook = "\n# v6.1j: Pharmaceutical Chemistry, ADME/PK, BCS & Drug Delivery Reference\npython3 pipeline/build_adme.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/adme"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/adme")\n'
        'def api_adme():\n'
        '    return _read_json(SITE_DIR / "data" / "adme.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"adme.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    adme_ref = _load(data_dir / "adme.json", {}) or {}\n'
        '    for sec_key, sec_q in [("adme_pillars", "adme"), ("pk_parameters", "pk"), ("bcs_classes", "bcs"), ("medchem_rules", "medchem"), ("ddis_and_pops", "ddis"), ("delivery_tech", "delivery")]:\n'
        '        for item in (adme_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "adme_pk",\n'
        '                "group": "ADME/PK, MedChem & Drug Delivery",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/adme?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/adme?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"ADME PK {sec_key} {item.get(\'name\', \'\')} {item.get(\'symbol\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')} {item.get(\'examples\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"adme", "#/ref/adme"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    adme_doc = _load_json(data_dir / "adme.json")\n'
        '    if isinstance(adme_doc, dict) and adme_doc.get("adme_pillars"):\n'
        '        a_lis = "".join(f\'<li><b>{_esc(p["name"])}</b> — {_esc(p.get("plain",""))}</li>\' for p in adme_doc["adme_pillars"])\n'
        '        pages.append(("adme", "#/ref/adme", "Pharmaceutical Chemistry, ADME/PK, BCS & Drug Delivery",\n'
        '                      "Primary-sourced reference on ADME pillars, PK equations (t1/2, CL, Vd, AUC), ICH M9 BCS Classes I–IV, Lipinski/bRo5 rules, CYP450 DDIs, and drug-delivery engineering.",\n'
        '                      f"<ul>{a_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/adme"' in txt:
        return False
    for anchor in ('    "/#/explore/trials",', '    "/#/explore/pathways",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/adme",\n    "/#/explore/adme",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_adme_py": _write_if_changed(pipe_dir / "build_adme.py", BUILD_ADME_PY),
        "adme_js": _write_if_changed(js_dir / "adme.js", ADME_JS),
        "app_js_wired": _patch_app_js(js_dir / "app.js"),
        "layout_js_wired": _patch_layout_js(js_dir / "layout.js"),
        "run_all_sh_hooked": _patch_run_all(pipe_dir / "run_all.sh"),
        "app_py_api_added": _patch_app_py(root / "app.py"),
        "global_search_indexed": _patch_global_search(pipe_dir / "build_global_search.py"),
        "static_seo_added": _patch_static_pages(pipe_dir / "build_v60_static_pages.py"),
        "test_v60_site_updated": _patch_test_v60_site(root / "tests" / "test_v60_site.py"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        (root / "site" / "data").mkdir(parents=True)
        (root / "tests").mkdir()

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/trials") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/trials", "Clinical trials & endpoints"]] }];\nconst EXPLORE_NAV = [["#/explore/trials", "Clinical trials & endpoints"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/trials",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_adme.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_adme.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"adme_pillars": 4, "pk_parameters": 6, "bcs_classes": 4, "medchem_rules": 5, "ddis_and_pops": 5, "delivery_tech": 6}, out

        doc = json.loads((root / "site" / "data" / "adme.json").read_text(encoding="utf-8"))
        for k in ("adme_pillars", "pk_parameters", "bcs_classes", "medchem_rules", "ddis_and_pops", "delivery_tech"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61J_ADME_PK_MEDCHEM_DELIVERY_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1j ADME/PK, MedChem & Drug Delivery patch.")
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
