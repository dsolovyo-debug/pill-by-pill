#!/usr/bin/env python3
"""Pill by Pill v6.1e Patch: Browsable WHO ATC Therapeutic Class Tree (#/ref/classes) & Origin Stories Batch 8 (75 -> 90).

1. Adds `pipeline/build_atc_tree.py` -> `site/data/atc_tree.json` aggregating all tagged medicines
   across the 14 official WHO ATC Level-1 organ systems (A–V) and Level-2 therapeutic subgroups.
2. Adds `site/js/atc_classes.js` (`atcClassesPage`) and wires `#/ref/classes`, `/api/classes`,
   `REF_NAV` / `REF_NAV_GROUPS`, and `pipeline/run_all.sh`.
3. Appends 15 primary-sourced landmark origin stories (Batch 8, checked 2026-11-22 against PMC)
   to `pipeline/origin_stories.json` (75 -> 90 total, idempotently deduplicated).

Usage:
  python3 2026-11-22_v6.1e_atc_class_tree_and_origins_batch8_patch.py --selftest
  python3 2026-11-22_v6.1e_atc_class_tree_and_origins_batch8_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_ATC_TREE_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1e Browsable WHO ATC Therapeutic Class Tree (`site/data/atc_tree.json`).\n\nScans `site/data/drugs/*.json` and deterministically aggregates every medicine with WHO ATC\ncode(s) into the 14 official WHO ATC Level-1 Anatomical Main Groups (A–V) and Level-2\nTherapeutic Subgroups (e.g., C09, J01, L01, N05). Zero fabricated classifications.\n\nUsage:\n  python3 pipeline/build_atc_tree.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-22"\n\nATC_LEVEL1 = {\n    "A": "Alimentary tract and metabolism",\n    "B": "Blood and blood forming organs",\n    "C": "Cardiovascular system",\n    "D": "Dermatologicals",\n    "G": "Genito-urinary system and sex hormones",\n    "H": "Systemic hormonal preparations, excl. sex hormones and insulins",\n    "J": "Antiinfectives for systemic use",\n    "L": "Antineoplastic and immunomodulating agents",\n    "M": "Musculo-skeletal system",\n    "N": "Nervous system",\n    "P": "Antiparasitic products, insecticides and repellents",\n    "R": "Respiratory system",\n    "S": "Sensory organs",\n    "V": "Various",\n}\n\n\ndef _extract_atc_codes(d: dict) -> list:\n    raw = d.get("atc") or d.get("atc_codes") or []\n    if isinstance(raw, str):\n        raw = [raw]\n    out = []\n    for item in raw:\n        code = item.get("code") if isinstance(item, dict) else item\n        s = str(code or "").strip().upper()\n        if len(s) >= 3 and s[0] in ATC_LEVEL1:\n            out.append(s)\n    return sorted(set(out))\n\n\ndef build_atc_tree(data_dir: pathlib.Path) -> dict:\n    drugs_dir = data_dir / "drugs"\n    groups = {\n        k: {"code": k, "name": v, "drug_ids": set(), "eml_count": 0, "subgroups": {}}\n        for k, v in ATC_LEVEL1.items()\n    }\n    total_tagged_drugs = 0\n\n    if drugs_dir.is_dir():\n        for fp in sorted(drugs_dir.glob("*.json")):\n            try:\n                d = json.loads(fp.read_text(encoding="utf-8"))\n            except Exception:\n                continue\n            codes = _extract_atc_codes(d)\n            if not codes:\n                continue\n            total_tagged_drugs += 1\n            slug = str(d.get("id") or fp.stem)\n            name = str(d.get("name") or slug)\n            is_eml = bool(d.get("who_eml"))\n            seen_l1 = set()\n            for code in codes:\n                l1 = code[0]\n                l2 = code[:3]\n                g = groups[l1]\n                if slug not in g["drug_ids"]:\n                    g["drug_ids"].add(slug)\n                    if is_eml and l1 not in seen_l1:\n                        g["eml_count"] += 1\n                        seen_l1.add(l1)\n                sg = g["subgroups"].setdefault(l2, {"code": l2, "drugs": []})\n                if not any(x["id"] == slug for x in sg["drugs"]):\n                    sg["drugs"].append({"id": slug, "name": name, "atc": code, "eml": is_eml})\n\n    out_groups = []\n    total_subgroups = 0\n    for k in sorted(ATC_LEVEL1.keys()):\n        g = groups[k]\n        sgs = []\n        for l2 in sorted(g["subgroups"].keys()):\n            sg = g["subgroups"][l2]\n            sg["drugs"].sort(key=lambda x: x["name"].lower())\n            sgs.append({\n                "code": l2,\n                "count": len(sg["drugs"]),\n                "drugs": sg["drugs"],\n            })\n        total_subgroups += len(sgs)\n        out_groups.append({\n            "code": k,\n            "name": g["name"],\n            "count": len(g["drug_ids"]),\n            "eml_count": g["eml_count"],\n            "subgroups": sgs,\n        })\n\n    payload = {\n        "checked": CHECKED,\n        "source": "WHO Collaborating Centre for Drug Statistics Methodology (ATC/DDD Index — non-commercial educational reference)",\n        "url": "https://atcddd.fhi.no/atc_ddd_index/",\n        "tagged_drugs": total_tagged_drugs,\n        "level1_groups": len(out_groups),\n        "level2_subgroups": total_subgroups,\n        "groups": out_groups,\n    }\n    data_dir.mkdir(parents=True, exist_ok=True)\n    (data_dir / "atc_tree.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "tagged_drugs": total_tagged_drugs,\n        "level1_groups": len(out_groups),\n        "level2_subgroups": total_subgroups,\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_atc_tree(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
ATC_CLASSES_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nexport async function atcClassesPage(query) {\n  const doc = await getJSON("data/atc_tree.json");\n  const groups = doc.groups || [];\n  const selGroup = ((query && query.get("group")) || "").toUpperCase();\n  const q = ((query && query.get("q")) || "").trim().toLowerCase();\n\n  const shownGroups = groups.filter((g) => {\n    if (selGroup && g.code !== selGroup) return false;\n    if (q) {\n      const hay = `${g.code} ${g.name} ${(g.subgroups || []).map((s) => `${s.code} ${(s.drugs || []).map((d) => d.name).join(" ")}`).join(" ")}`.toLowerCase();\n      return hay.includes(q);\n    }\n    return true;\n  });\n\n  return {\n    title: "WHO ATC Therapeutic Class Tree",\n    body: html`\n      <h1>WHO ATC Therapeutic Class Tree</h1>\n      <p class="lead">Browse medicines by the 14 WHO Anatomical Therapeutic Chemical (ATC) Level-1 organ systems and Level-2 therapeutic subgroups (${doc.tagged_drugs || 0} tagged medicines across ${doc.level2_subgroups || 0} subgroups; checked ${doc.checked}).</p>\n      <p class="small">Jump to system:\n        <a href="#/ref/classes"${!selGroup ? \' aria-current="page"\' : ""}>All 14 Systems</a>\n        ${groups.map((g) => html` · <a href="#/ref/classes?group=${g.code}"${selGroup === g.code ? \' aria-current="page"\' : ""}><b>${g.code}</b> (${g.count})</a>`)}\n      </p>\n      ${shownGroups.map((g) => html`\n        <section class="x-panel" id="atc-${g.code}">\n          <h2>${g.code} — ${g.name} <span class="muted small">(${g.count} medicines${g.eml_count ? ` · ${g.eml_count} WHO EML` : ""})</span></h2>\n          ${(g.subgroups || []).length ? html`\n            <div class="tbl-wrap" tabindex="0" role="region" aria-label="ATC ${g.code} subgroups">\n              <table class="tbl"><thead><tr><th>Subgroup</th><th>Count</th><th>Medicines</th></tr></thead>\n              <tbody>${g.subgroups.map((sg) => html`<tr>\n                <td><b>${sg.code}</b></td>\n                <td>${sg.count}</td>\n                <td>${(sg.drugs || []).slice(0, 18).map((d) => html`<a href="#/ref/drug/${d.id}">${d.name}</a>${d.eml ? " ★" : ""}`).join(" · ")}${sg.drugs.length > 18 ? html` <span class="muted small">(+${sg.drugs.length - 18} more)</span>` : ""}</td>\n              </tr>`)}</tbody></table>\n            </div>\n          ` : html`<p class="muted small">No medicines tagged in this group in the current build.</p>`}\n        </section>\n      `)}\n      <p class="muted small">Source: <a href="${doc.url}" target="_blank" rel="noopener">${doc.source}</a>. ★ = on WHO Model List of Essential Medicines.</p>\n    `,\n  };\n}\n'
BATCH8_ORIGINS = [{'medicine': 'RIFAMPIN', 'category': 'Semi-synthetic natural product', 'simple': 'In 1957, Piero Sensi and colleagues isolated a soil bacterium (now called Amycolatopsis rifamycinica) from a pine forest sample, giving rise to the rifamycin antibiotics—and chemically modifying it produced rifampin, a cornerstone pill for tuberculosis.', 'expert': 'Derived from rifamycins discovered in 1957 by Piero Sensi and colleagues at Lepetit from Streptomyces mediterranei (now Amycolatopsis rifamycinica), rifampin (rifampicin) is a semi-synthetic ansamycin antibiotic that inhibits bacterial DNA-dependent RNA polymerase.', 'sources': [{'label': 'CDC Emerging Infectious Diseases — Etymologia: Rifampin (PMC5823362)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC5823362/'}], 'checked': '2026-11-22'}, {'medicine': 'ISONIAZID', 'category': 'Rediscovered synthetic', 'simple': 'Two PhD students in Prague first synthesized isoniazid in 1912 with no idea it could fight disease—until 1951, when three pharmaceutical labs independently discovered its extraordinary power against tuberculosis, leading to FDA approval in 1952.', 'expert': "First synthesized in 1912 by Hans Meyer and Josef Mally at German Charles University in Prague, isoniazid's potent antitubercular activity was independently demonstrated in 1951 by Hoffmann-La Roche, E.R. Squibb & Sons, and Bayer, earning FDA approval in 1952; bacterial KatG activates it to an INH-NAD+ adduct blocking mycolic acid synthesis.", 'sources': [{'label': 'PMC6965675 — Isoniazid and host immune system interactions', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6965675/'}, {'label': 'PMC4526730 — Tuberculosis Drug Development: History and Evolution', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4526730/'}], 'checked': '2026-11-22'}, {'medicine': 'DOXYCYCLINE', 'category': 'Semi-synthetic natural product', 'simple': 'Building on natural tetracycline antibiotics found in soil bacteria in the late 1940s, Pfizer chemists removed a single oxygen-hydrogen group to make 6-deoxytetracyclines—creating doxycycline (1967), a more stable, longer-lasting broad-spectrum antibiotic.', 'expert': "Following Lederle's 1948 isolation of chlortetracycline and Pfizer's oxytetracycline, Pfizer chemists demonstrated reductive removal of the C6-hydroxyl group to yield acid-stable 6-deoxytetracyclines, culminating in the semi-synthetic antibiotic doxycycline (1967).", 'sources': [{'label': 'PMC2681267 — A Robust Platform for the Synthesis of New Tetracycline Antibiotics', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC2681267/'}, {'label': 'PMC8707899 — The Development of Third-Generation Tetracycline Antibiotics', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8707899/'}], 'checked': '2026-11-22'}, {'medicine': 'CEPHALEXIN', 'category': 'Semi-synthetic natural product', 'simple': 'The cephalosporin family started in 1945 when Italian scientist Giuseppe Brotzu isolated an antibacterial mold in Sardinia—and chemists later turned its cephalosporin C scaffold into cephalexin (launched 1969–1970), one of the first widely used oral cephalosporin antibiotics.', 'expert': 'Cephalexin is a first-generation semi-synthetic oral cephalosporin derived from the cephalosporin C nucleus discovered in 1945 by Giuseppe Brotzu from a mold in Sardinia, Italy, and introduced clinically in 1969–1970 (Keflex/Ceporex).', 'sources': [{'label': 'PMC2657229 — Cephalosporins discovery by Giuseppe Brotzu (1945)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC2657229/'}, {'label': 'PMC13471034 — Etymology and History of Antibacterials', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC13471034/'}, {'label': 'PMC9092475 — Prescribed drugs containing nitrogen heterocycles', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9092475/'}], 'checked': '2026-11-22'}, {'medicine': 'PREDNISONE', 'category': 'Semi-synthetic steroid', 'simple': 'After Edward Kendall isolated cortisone and Philip Hench used it to treat rheumatoid arthritis in 1948, scientists at Schering Corporation modified cortisone in the 1950s to create prednisone, a more potent oral steroid with less salt retention.', 'expert': "Building on Edward Kendall's isolation of adrenal Compound E (cortisone) and Philip Hench's 1948 rheumatoid arthritis milestone, Arthur Nobile and colleagues at Schering Corporation discovered the delta-1,4-steroids prednisone and prednisolone in the 1950s as higher-potency synthetic glucocorticoids.", 'sources': [{'label': 'PMC7550368 — A Short History of Glucocorticoids', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7550368/'}, {'label': 'PMC4885377 — History of Nephrotic Syndrome (citing Nobile, Schering discovery)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4885377/'}], 'checked': '2026-11-22'}, {'medicine': 'AMLODIPINE', 'category': 'Medicinal chemistry', 'simple': 'Building on earlier short-acting dihydropyridine blood-pressure pills like nifedipine, Pfizer researchers developed amlodipine in the 1980s as a slow-onset, once-daily calcium channel blocker that relaxes blood vessels smoothly.', 'expert': 'Developed by Pfizer (reported by Burges et al., 1987) as a long-acting dihydropyridine calcium channel blocker following nifedipine, amlodipine blocks L-type (and N-type) voltage-operated calcium channels with gradual vascular relaxation and once-daily dosing.', 'sources': [{'label': 'PMC5447095 — Discovery and Development of Calcium Channel Blockers', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC5447095/'}], 'checked': '2026-11-22'}, {'medicine': 'LISINOPRIL', 'category': 'Structure-guided design', 'simple': "To avoid side effects of the first ACE inhibitor captopril, Arthur Patchett's team at Merck designed non-thiol blockers—swapping in the amino acid lysine to create lisinopril (approved 1987), an oral blood-pressure pill that works directly without needing liver activation.", 'expert': "Emerging from Arthur Patchett et al.'s (1980) non-sulfhydryl ACE inhibitor program at Merck, lisinopril replaces the alanine of enalaprilat with lysine, imparting direct oral bioavailability without an ester prodrug; patented in 1978 and FDA-approved in 1987.", 'sources': [{'label': 'PMC2690933 — Medicinal Chemistry of Angiotensin-Converting Enzyme Inhibitors', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC2690933/'}, {'label': 'PMC3565918 — ACE inhibitors & Patchett et al. (1980)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC3565918/'}, {'label': 'PMC9092475 — Prescribed drugs containing nitrogen heterocycles', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9092475/'}], 'checked': '2026-11-22'}, {'medicine': 'LEVOTHYROXINE SODIUM', 'category': 'Hormone replacement', 'simple': 'Edward Kendall isolated the thyroid hormone thyroxine on Christmas Day in 1914, and in 1926 Charles Harington and George Barger solved its chemical structure and synthesized it—paving the way for levothyroxine, one of the most prescribed pills in the world.', 'expert': 'Thyroxine was isolated by Edward Calvin Kendall on December 25, 1914; its chemical structure was determined and synthesized in 1926 by Charles Harington and George Barger, establishing synthetic levothyroxine sodium as standard thyroid hormone replacement.', 'sources': [{'label': 'PMC3046199 — The discovery of thyroid replacement therapy', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC3046199/'}, {'label': 'PMC10801080 — Levothyroxine personalized treatment (historical background)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10801080/'}], 'checked': '2026-11-22'}, {'medicine': 'CARBAMAZEPINE', 'category': 'Medicinal chemistry', 'simple': 'While exploring tricyclic compounds in Basel, Switzerland, chemist Walter Schindler at J.R. Geigy discovered carbamazepine in 1953—a molecule that became a mainstay medicine for epilepsy and trigeminal nerve pain.', 'expert': 'Discovered in 1953 by chemist Walter Schindler (with Blattner) at J.R. Geigy AG in Basel, Switzerland during tricyclic neuroleptic research, carbamazepine was synthesized for clinical development in 1960 and became a frontline sodium-channel anti-seizure medication.', 'sources': [{'label': 'PMC4158257 — Highlights in the History of Epilepsy: The Last 200 Years', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4158257/'}, {'label': 'PMC5762214 — Carbamazepine discovery background', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC5762214/'}], 'checked': '2026-11-22'}, {'medicine': 'ONDANSETRON', 'category': 'Selective receptor design', 'simple': 'Glaxo scientists originally investigated ondansetron (GR38032F) for migraine and brain disorders, but blocking the serotonin 5-HT3 receptor proved transformative for preventing severe nausea and vomiting from cancer chemotherapy and surgery.', 'expert': 'Identified by Glaxo as GR38032F initially for migraine and CNS indications, ondansetron proved to be a selective 5-HT3 receptor antagonist that revolutionized control of chemotherapy-, radiation-, and surgery-induced emesis.', 'sources': [{'label': 'PMC6131675 — A History of Drug Discovery for Treatment of Nausea and Vomiting', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6131675/'}, {'label': 'PMC6741689 — Ondansetron: A Selective 5-HT3 Receptor Antagonist', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6741689/'}], 'checked': '2026-11-22'}, {'medicine': 'ALLOPURINOL', 'category': 'Rational drug design', 'simple': 'Gertrude Elion and George Hitchings created allopurinol while trying to slow down how fast the body broke down a leukemia drug—and discovered it blocked uric acid production so well that the FDA approved it for gout in 1966.', 'expert': 'Developed by Gertrude B. Elion, George H. Hitchings, and colleagues (Biochem Pharmacol 1963) as a purine analog inhibiting xanthine oxidase-catalyzed drug degradation, allopurinol blocked uric acid formation and received FDA approval for gout in 1966.', 'sources': [{'label': 'PMC2233605 — Therapeutic Effects of Xanthine Oxidase Inhibitors', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC2233605/'}, {'label': 'PMC2697767 — Allopurinol background (citing Elion & Hitchings 1963)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC2697767/'}], 'checked': '2026-11-22'}, {'medicine': 'KETAMINE', 'category': 'Medicinal chemistry', 'simple': 'In 1962, organic chemist Calvin Stevens at Wayne State University (consulting for Parke-Davis) synthesized compound CI-581—ketamine—creating a fast-acting surgical anesthetic that keeps patients breathing on their own.', 'expert': 'First synthesized in 1962 as CI-581 by organic chemist Professor Calvin Lee Stevens at Wayne State University while consulting for Parke-Davis, ketamine was developed as a shorter-acting dissociative anesthetic and NMDA receptor antagonist.', 'sources': [{'label': 'PMC6493431 — Happy 50th Anniversary Ketamine', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6493431/'}, {'label': 'PMC5126726 — Ketamine: 50 Years of Modulating the Mind', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC5126726/'}], 'checked': '2026-11-22'}, {'medicine': 'FENTANYL', 'category': 'Medicinal chemistry', 'simple': 'In 1960, Belgian chemist Paul Janssen systematically modified older synthetic painkillers like meperidine and phenoperidine to build fentanyl—an ultra-potent surgical painkiller and anesthetic first approved in the US in 1968.', 'expert': 'Synthesized around 1960 by Dr. Paul Janssen in Belgium through structure-activity optimization of meperidine and phenoperidine, fentanyl entered European surgical practice within three years and was introduced in the United States in 1968 under strict perioperative controls.', 'sources': [{'label': 'PMC4137794 — Fentanyl-related compounds and derivatives', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4137794/'}, {'label': 'PMC10016219 — Brief History of Opioids in Perioperative Management', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10016219/'}], 'checked': '2026-11-22'}, {'medicine': 'METRONIDAZOLE', 'category': 'Natural-product-inspired synthetic', 'simple': "Scientists at Rhône-Poulenc in France designed metronidazole from the bacterial compound azomycin to treat a parasitic infection in 1959—then accidentally discovered in 1962 that it also cured a patient's bacterial gum infection, unlocking its use against anaerobic bacteria.", 'expert': "Developed at Rhône-Poulenc in France as a synthetic nitroimidazole derivative of the Streptomyces natural product azomycin for Trichomonas vaginalis (1959), metronidazole's anaerobic antibacterial activity was discovered serendipitously in 1962 when it simultaneously cured bacterial gingivitis.", 'sources': [{'label': 'PMC89320 — Why Metronidazole Is Active against both Bacteria and Parasites', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC89320/'}, {'label': 'PMC12150256 — Novel Metronidazole Conjugates (azomycin origin)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12150256/'}], 'checked': '2026-11-22'}, {'medicine': 'VENETOCLAX', 'category': 'Fragment-based NMR design', 'simple': "Using powerful NMR magnets to spot tiny chemical fragments sticking to a 'hard-to-drug' cancer survival protein, scientists engineered venetoclax (ABT-199)—the first approved pill designed specifically to block BCL-2 and trigger leukemia cells to self-destruct.", 'expert': 'Built via NMR-guided fragment-based drug discovery (FBDD) and structure-guided redesign of navitoclax to spare BCL-XL (avoiding thrombocytopenia), venetoclax (ABT-199) became the first approved selective BCL-2 BH3-mimetic targeting a protein-protein interaction.', 'sources': [{'label': 'PMC8895297 — Fragment-Based Drug Discovery by NMR (Venetoclax / ABT-199 case study)', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8895297/'}, {'label': 'PMC8589430 — Discovery, development and application of drugs targeting BCL-2', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8589430/'}], 'checked': '2026-11-22'}]


def _write_if_changed(path: pathlib.Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def _patch_origin_stories(path: pathlib.Path) -> int:
    if not path.is_file():
        return 0
    doc = json.loads(path.read_text(encoding="utf-8"))
    stories = doc.get("stories") if isinstance(doc, dict) else doc
    if not isinstance(stories, list):
        raise ValueError(f"Unexpected origin_stories.json structure in {path}")
    existing = {str(s.get("medicine", "")).strip().upper() for s in stories}
    added = 0
    for entry in BATCH8_ORIGINS:
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


def _patch_app_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    imp = 'import { atcClassesPage } from "./atc_classes.js";\n'
    if "./atc_classes.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/classes"' not in txt:
        for anchor in ('if (path === "/explore/worksheets")', 'if (path === "/glossary"', 'if (path === "/search"', 'if (path === "/ref/equipment")'):
            if anchor in txt:
                rep = 'if (path === "/ref/classes") return atcClassesPage(query);\n  ' + anchor
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
    if "#/ref/classes" in txt:
        return False
    changed = False
    anchor1 = '["#/ref/families", "Families"]'
    if anchor1 in txt:
        txt = txt.replace(anchor1, anchor1 + ',\n      ["#/ref/classes", "ATC classes"]', 1)
        changed = True
    anchor2 = '["#/ref/search", "Global search"]'
    if not changed and anchor2 in txt:
        txt = txt.replace(anchor2, anchor2 + ',\n  ["#/ref/classes", "ATC classes"]', 1)
        changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_atc_tree.py" in txt:
        return False
    hook = "\n# v6.1e: Browsable WHO ATC Therapeutic Class Tree\npython3 pipeline/build_atc_tree.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/classes"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/classes")\n'
        'def api_atc_classes():\n'
        '    return _read_json(SITE_DIR / "data" / "atc_tree.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_atc_tree_py": _write_if_changed(pipe_dir / "build_atc_tree.py", BUILD_ATC_TREE_PY),
        "atc_classes_js": _write_if_changed(js_dir / "atc_classes.js", ATC_CLASSES_JS),
        "batch8_origin_stories_added": _patch_origin_stories(pipe_dir / "origin_stories.json"),
        "app_js_wired": _patch_app_js(js_dir / "app.js"),
        "layout_js_wired": _patch_layout_js(js_dir / "layout.js"),
        "run_all_sh_hooked": _patch_run_all(pipe_dir / "run_all.sh"),
        "app_py_api_added": _patch_app_py(root / "app.py"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        (root / "site" / "data" / "drugs").mkdir(parents=True)

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/explore/worksheets") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('export const REF_NAV_GROUPS = [{ items: [["#/ref/families", "Families"]] }];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        seed = {"stories": [{"medicine": f"DRUG_{i}", "category": "Test", "simple": "a", "expert": "b", "sources": [{"label": "s", "url": "https://example.org"}], "checked": "2026-11-21"} for i in range(75)]}
        (root / "pipeline" / "origin_stories.json").write_text(json.dumps(seed), encoding="utf-8")
        (root / "site" / "data" / "drugs" / "lisinopril.json").write_text(json.dumps({"id": "lisinopril", "name": "Lisinopril", "atc": ["C09AA03"], "who_eml": True}), encoding="utf-8")
        (root / "site" / "data" / "drugs" / "venetoclax.json").write_text(json.dumps({"id": "venetoclax", "name": "Venetoclax", "atc": ["L01XX52"], "who_eml": False}), encoding="utf-8")

        r1 = apply_patch(root)
        assert r1["batch8_origin_stories_added"] == 15 and all(v for k, v in r1.items() if k != "batch8_origin_stories_added"), r1
        r2 = apply_patch(root)
        assert r2["batch8_origin_stories_added"] == 0 and not any(v for k, v in r2.items() if k != "batch8_origin_stories_added"), r2

        py_compile.compile(str(root / "pipeline" / "build_atc_tree.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_atc_tree.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out["tagged_drugs"] == 2 and out["level1_groups"] == 14 and out["level2_subgroups"] == 2, out

        doc = json.loads((root / "pipeline" / "origin_stories.json").read_text(encoding="utf-8"))
        assert len(doc["stories"]) == 90, len(doc["stories"])
        for s in doc["stories"][-15:]:
            assert s["checked"] == "2026-11-22" and s["sources"] and all(u["url"].startswith("https://") for u in s["sources"])

        print("V61E_ATC_TREE_AND_ORIGINS_BATCH8_SELFTEST_PASSED", json.dumps({**out, "total_stories": len(doc["stories"]), **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1e ATC Class Tree & Origin Stories Batch 8 patch.")
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
