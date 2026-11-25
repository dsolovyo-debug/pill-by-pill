#!/usr/bin/env python3
"""Pill by Pill v6.1c Patch: Copy SMILES/InChIKey + Chem Props, Quiz Topic/Length Filters & Native Printable Teacher Worksheets.

Closes the remaining P2 items from the 2026-11-21 Blind 6-Role Audit:
  1. Chemical Tools (`site/js/chem_tools.js`): 1-click Copy SMILES / InChIKey / ChEMBL ID
     buttons + physicochemical properties strip (MW, ALogP, PSA, HBD, HBA, Ro5 — strictly
     rendered only when present on the drug record; zero fabricated figures).
  2. Quiz Topic & Length Filters (`site/js/quiz_filters.js`): Deterministic topic classifier
     (History / Science / Pharma Operations) + Quick 10 / Standard 20 / Full length switcher.
  3. Native Printable Teacher Worksheets (`pipeline/build_worksheets.py` -> `site/data/worksheets.json`,
     `site/js/worksheets.js`, `#/explore/worksheets`, `/api/worksheets`): 4 NGSS & AP Biology
     aligned worksheets with Print button and toggleable Teacher Answer Key (zero commercial links).

Usage:
  python3 2026-11-22_v6.1c_chem_copy_quiz_filters_teacher_worksheets_patch.py --selftest
  python3 2026-11-22_v6.1c_chem_copy_quiz_filters_teacher_worksheets_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_WORKSHEETS_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1c Native Printable Teacher Worksheets (`site/data/worksheets.json`).\n\nGenerates 4 classroom-ready, zero-ad, zero-commercial-link printable worksheets aligned to\nNGSS and AP Biology standards, each with student write-in prompts, direct Pill by Pill\nExplore links, and a toggleable Teacher Answer Key.\n\nUsage:\n  python3 pipeline/build_worksheets.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-22"\n\nWORKSHEETS = [\n    {\n        "id": "ws-plant-to-pill",\n        "title": "Worksheet 1: From Nature to Medicine & Drug Name Decoding",\n        "grade_band": "Grades 7–12 · General Biology / Chemistry",\n        "standards": ["NGSS HS-LS1-1", "NGSS HS-PS1-2"],\n        "estimated_time": "30–40 minutes",\n        "explore_links": [\n            {"label": "Origin Stories Gallery (75)", "href": "#/explore/origins"},\n            {"label": "How Medicines Are Made", "href": "#/explore/made"},\n        ],\n        "questions": [\n            {\n                "prompt": "Pick two medicines from the Origin Stories Gallery that started in a plant, fungus, or soil bacterium. Record the original organism, the active medicine, and why chemists still study or modify natural molecules.",\n                "answer": "Examples include aspirin (willow bark -> salicin -> acetylsalicylic acid), paclitaxel (Pacific yew / Taxus cell fermentation), penicillin G (Penicillium chrysogenum), lovastatin (Aspergillus terreus), or empagliflozin (inspired by apple-bark phlorizin). Chemists modify natural scaffolds to improve stability, absorption, potency, or scalable supply.",\n            },\n            {\n                "prompt": "Compare a Small Molecule pill with a Monoclonal Antibody (-mab) on the \'5 Types of Modern Medicines\' page. Why can most small molecules be swallowed as pills while antibodies must be injected or infused?",\n                "answer": "Small molecules (<500–900 Da) are chemically stable enough to survive stomach acid and cross the gut wall. Monoclonal antibodies (~150,000 Da proteins) would be digested into amino acids in the stomach and are too large to pass intact through the intestinal lining.",\n            },\n            {\n                "prompt": "Look up three medicines sharing the same INN stem (such as -vastatin, -mab, or -tinib). What does a shared stem tell pharmacists and doctors?",\n                "answer": "WHO/USAN INN stems indicate a shared chemical or pharmacological class (e.g., -vastatin = HMG-CoA reductase inhibitors; -mab = monoclonal antibodies; -tinib = tyrosine kinase inhibitors), reducing prescribing errors.",\n            },\n        ],\n    },\n    {\n        "id": "ws-3d-binding",\n        "title": "Worksheet 2: Inside the 3D Binding Pocket (Structure & Function)",\n        "grade_band": "Grades 10–12 · AP Biology / Honors Chemistry",\n        "standards": ["AP Biology Unit 3 (Enzyme Catalysis)", "NGSS HS-LS1-1"],\n        "estimated_time": "35–45 minutes",\n        "explore_links": [\n            {"label": "Trace Imatinib End-to-End", "href": "#/explore/trace?drug=imatinib"},\n            {"label": "Discovery & Preclinical Guide", "href": "#/explore/departments/discovery"},\n        ],\n        "questions": [\n            {\n                "prompt": "Open a medicine with an experimental 3D binding animation (such as imatinib, atorvastatin, or semaglutide). Name the target protein and identify the experimental method (X-ray crystallography or cryo-EM) used to capture the structure.",\n                "answer": "Imatinib binds ABL1 tyrosine kinase (X-ray); atorvastatin binds HMG-CoA reductase (X-ray, PDB 1HWK); semaglutide binds the GLP-1 receptor (X-ray/cryo-EM, PDB 4ZGM).",\n            },\n            {\n                "prompt": "Explain how non-covalent interactions (hydrogen bonds, hydrophobic contacts, or metal coordination) vs. covalent bonds hold a drug inside its target pocket.",\n                "answer": "Most drugs bind reversibly through complementary 3D shape and non-covalent contacts (polar hydrogen bonds, non-polar hydrophobic packing, or metal coordination). Covalent inhibitors (such as sotorasib or osimertinib) form a permanent chemical bond with a specific amino acid like cysteine.",\n            },\n            {\n                "prompt": "Why does Pill by Pill label the fly-in motion as an illustration while noting that the final bound pose and residue contacts come from real Protein Data Bank (PDB) experiments?",\n                "answer": "Crystal and cryo-EM structures capture static snapshots of the bound state; the fly-in path helps students visualize entry into the active site, whereas the final coordinates and measured contact distances reflect real experimental data.",\n            },\n        ],\n    },\n    {\n        "id": "ws-8stage-lifecycle",\n        "title": "Worksheet 3: Tracing One Medicine Across the 8-Stage Lifecycle",\n        "grade_band": "Grades 9–12 · Biotechnology / Health Careers",\n        "standards": ["NGSS HS-ETS1-2", "NGSS HS-ETS1-3"],\n        "estimated_time": "40–50 minutes",\n        "explore_links": [\n            {"label": "8-Stage Lifecycle Guide", "href": "#/explore/how-drugs-are-built"},\n            {"label": "Trace One Drug Storyboards", "href": "#/explore/trace"},\n            {"label": "Who Builds, Tests & Delivers Drugs", "href": "#/explore/partners"},\n        ],\n        "questions": [\n            {\n                "prompt": "Choose one storyboard (Imatinib, Semaglutide, or Patisiran). Summarize what happens to that medicine in Stage 2 (Formulation), Stage 4 (Clinical Trials), and Stage 8 (Distribution & Safety).",\n                "answer": "Example (Patisiran): Stage 2 encapsulates siRNA inside a 4-lipid nanoparticle (LNP); Stage 4 proved >80% TTR protein knockdown and clinical efficacy in the Phase 3 APOLLO trial; Stage 8 ships via 2–8°C cold-chain 3PL and specialty pharmacy to infusion clinics with ongoing pharmacovigilance.",\n            },\n            {\n                "prompt": "Why do Phase 2 clinical trials represent the biggest attrition bottleneck in drug development?",\n                "answer": "Phase 2 is the first time a candidate is tested in a larger group of patients with the target disease to see whether the biological hypothesis actually improves clinical outcomes at a tolerable dose; many candidates that looked safe in animals and Phase 1 fail to show sufficient efficacy in Phase 2.",\n            },\n            {\n                "prompt": "Name two specialized partner organizations (outside the original drug inventor) that help bring a medicine to patients, and state what each one does.",\n                "answer": "Examples: Contract Research Organizations (CROs) run hospital clinical trials under GCP; CDMOs manufacture APIs or sterile vials under cGMP; 3PLs and wholesalers manage cold-chain warehousing and daily pharmacy replenishment; Specialty Pharmacies manage complex dispensing and REMS safety programs.",\n            },\n        ],\n    },\n    {\n        "id": "ws-global-economics",\n        "title": "Worksheet 4: Global Approvals, Generics & Drug Economics",\n        "grade_band": "Grades 10–12 · AP Government / Economics / Health Science",\n        "standards": ["C3 Framework D2.Eco.1.9-12", "NGSS HS-ETS1-3"],\n        "estimated_time": "30–40 minutes",\n        "explore_links": [\n            {"label": "How Medicines Are Funded & Priced", "href": "#/explore/economics"},\n            {"label": "Acronym Glossary", "href": "#/explore/glossary"},\n        ],\n        "questions": [\n            {\n                "prompt": "List the four main funding stages from \'How New Medicines Are Funded & Priced\'. Who typically funds basic target discovery vs. global Phase 3 trials?",\n                "answer": "Public grants (NIH/NSF), universities, and foundations fund early basic science; venture capital funds preclinical/Phase 1–2 biotech startups; IPOs, Big Pharma licensing, and commercial operating cash flow fund global Phase 3 trials and worldwide launches.",\n            },\n            {\n                "prompt": "What is the difference between a drug\'s Wholesale Acquisition Cost (WAC) and Manufacturer Net Revenue? Name two deductions in the Gross-to-Net waterfall.",\n                "answer": "WAC is the published list price before discounts, while Net Revenue is what the manufacturer actually retains. Deductions include wholesaler distribution fees, commercial PBM formulary rebates, 340B discounts, Medicaid Best Price, and CMS Medicare Drug Price Negotiation.",\n            },\n            {\n                "prompt": "Using the Acronym Glossary, define IND, NDA, cGMP, and LOE in one plain-language sentence each.",\n                "answer": "IND: FDA permission to begin human trials; NDA: application to market a new drug; cGMP: strict factory quality rules; LOE: Loss of Exclusivity when patents/exclusivities expire and generic/biosimilar competition begins.",\n            },\n        ],\n    },\n]\n\n\ndef build_worksheets(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "count": len(WORKSHEETS),\n        "scope_note": "Free, ad-free classroom worksheets built for printing directly from the browser. Zero tracking and zero commercial links.",\n        "worksheets": WORKSHEETS,\n    }\n    (data_dir / "worksheets.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {"worksheets_count": len(WORKSHEETS)}\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_worksheets(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
CHEM_TOOLS_JS = 'import { html } from "./ui.js";\n\nexport function renderChemToolsHtml(d) {\n  if (!d) return "";\n  const smiles = d.smiles || (d.chem && d.chem.smiles) || "";\n  const inchikey = d.inchikey || (d.chem && d.chem.inchikey) || "";\n  const chemblId = d.chembl_id || "";\n  const props = [];\n  const src = d.props || d.chem || d;\n  if (src.mw != null) props.push(["MW", `${src.mw} Da`]);\n  if (src.alogp != null) props.push(["ALogP", String(src.alogp)]);\n  if (src.psa != null) props.push(["PSA", `${src.psa} Å²`]);\n  if (src.hbd != null) props.push(["HBD", String(src.hbd)]);\n  if (src.hba != null) props.push(["HBA", String(src.hba)]);\n  if (src.ro5 != null) props.push(["Lipinski Ro5 violations", String(src.ro5)]);\n\n  if (!smiles && !inchikey && !chemblId && !props.length) return "";\n  return html`\n    <section class="chem-tools x-panel" aria-label="Chemical identifiers and physicochemical properties">\n      <div class="chem-copy-bar">\n        ${smiles ? html`<button type="button" class="copy-chem-btn" data-copy="${smiles}" data-label="SMILES">Copy SMILES</button>` : ""}\n        ${inchikey ? html`<button type="button" class="copy-chem-btn" data-copy="${inchikey}" data-label="InChIKey">Copy InChIKey</button>` : ""}\n        ${chemblId ? html`<button type="button" class="copy-chem-btn" data-copy="${chemblId}" data-label="ChEMBL ID">Copy ${chemblId}</button>` : ""}\n        <span id="chem-copy-status" class="muted small" role="status" aria-live="polite"></span>\n      </div>\n      ${props.length ? html`<p class="muted small"><b>Physicochemical properties:</b> ${props.map(([k, v]) => `${k}: ${v}`).join(" · ")}</p>` : ""}\n    </section>\n  `;\n}\n\nexport function attachChemTools(rootEl = document) {\n  const btns = rootEl.querySelectorAll(".copy-chem-btn");\n  const status = rootEl.querySelector("#chem-copy-status");\n  btns.forEach((btn) => {\n    btn.addEventListener("click", async () => {\n      const val = btn.getAttribute("data-copy") || "";\n      const label = btn.getAttribute("data-label") || "Value";\n      try {\n        if (navigator.clipboard && navigator.clipboard.writeText) {\n          await navigator.clipboard.writeText(val);\n        }\n        if (status) status.textContent = `Copied ${label} to clipboard.`;\n      } catch (_) {\n        if (status) status.textContent = `${label}: ${val}`;\n      }\n    });\n  });\n}\n'
QUIZ_FILTERS_JS = 'import { html } from "./ui.js";\n\nexport function classifyQuizTopic(q) {\n  const txt = `${q.q || ""} ${q.explain || ""} ${q.source || ""}`.toLowerCase();\n  if (/21 cfr|ind |cbo|dscsa|glp|cro|wac|pbm|340b|ppq|cgmp|ectd|rems|nda|bla|anda/.test(txt)) {\n    return "operations";\n  }\n  if (/discover|nobel|century|19\\d\\d|18\\d\\d|bark|mold|fleming|elion|black|kelsey|history|ancient|papyrus/.test(txt)) {\n    return "history";\n  }\n  return "science";\n}\n\nexport function filterQuizQuestions(questions = [], { topic = "all", limit = 0 } = {}) {\n  const tagged = questions.map((q) => ({ ...q, _topic: q.topic || classifyQuizTopic(q) }));\n  const byTopic = topic && topic !== "all" ? tagged.filter((q) => q._topic === topic) : tagged;\n  return limit > 0 ? byTopic.slice(0, limit) : byTopic;\n}\n\nexport function renderQuizFilterBarHtml({ topic = "all", limit = 0, total = 0, baseRoute = "#/explore/quiz" } = {}) {\n  const mk = (t, l) => `${baseRoute}?topic=${encodeURIComponent(t)}&limit=${l}`;\n  return html`<p class="small quiz-filters" aria-label="Quiz topic and length filters">\n    Topic:\n    <a href="${mk("all", limit)}"${topic === "all" ? \' aria-current="page"\' : ""}>All (${total})</a> ·\n    <a href="${mk("history", limit)}"${topic === "history" ? \' aria-current="page"\' : ""}>History</a> ·\n    <a href="${mk("science", limit)}"${topic === "science" ? \' aria-current="page"\' : ""}>Science</a> ·\n    <a href="${mk("operations", limit)}"${topic === "operations" ? \' aria-current="page"\' : ""}>Pharma Operations</a>\n    &nbsp;|&nbsp; Length:\n    <a href="${mk(topic, 10)}"${limit === 10 ? \' aria-current="page"\' : ""}>Quick 10</a> ·\n    <a href="${mk(topic, 20)}"${limit === 20 ? \' aria-current="page"\' : ""}>Standard 20</a> ·\n    <a href="${mk(topic, 0)}"${limit === 0 ? \' aria-current="page"\' : ""}>Full</a>\n  </p>`;\n}\n'
WORKSHEETS_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nexport async function worksheetsPage(query) {\n  const doc = await getJSON("data/worksheets.json");\n  const all = doc.worksheets || [];\n  const sel = (query && query.get("id")) || (all[0] && all[0].id) || "";\n  const active = all.find((w) => w.id === sel) || all[0];\n\n  return {\n    title: active ? `Printable Worksheet: ${active.title}` : "Teacher Worksheets",\n    body: html`\n      <h1>Printable Classroom Worksheets (NGSS &amp; AP Biology)</h1>\n      <p class="lead">${doc.scope_note}</p>\n      <p class="small no-print">Select worksheet:\n        ${all.map((w) => html`<a href="#/explore/worksheets?id=${w.id}"${w.id === active.id ? \' aria-current="page"\' : ""}><b>${w.title.split(":")[0]}</b></a>`).join(" · ")}\n      </p>\n      <p class="no-print">\n        <button id="ws-print-btn" type="button">Print Worksheet</button>\n        <button id="ws-key-btn" type="button" aria-expanded="false">Show Teacher Answer Key</button>\n      </p>\n      ${active ? html`\n        <article class="x-panel worksheet-sheet">\n          <h2>${active.title}</h2>\n          <p class="muted small">${active.grade_band} · ${active.estimated_time} · Standards: ${(active.standards || []).join(", ")}</p>\n          <p class="small no-print">Explore links for students: ${(active.explore_links || []).map((l) => html`<a href="${l.href}">${l.label}</a>`).join(" · ")}</p>\n          <p class="small"><b>Student Name:</b> ____________________________ &nbsp;&nbsp; <b>Date:</b> ________________</p>\n          <ol>${(active.questions || []).map((q, idx) => html`\n            <li style="margin-bottom:1.25rem">\n              <p><b>Q${idx + 1}.</b> ${q.prompt}</p>\n              <div class="ws-lines" aria-hidden="true" style="border-bottom:1px solid var(--line,#cbd5e1);height:2rem;margin-bottom:0.6rem"></div>\n              <div class="ws-lines" aria-hidden="true" style="border-bottom:1px solid var(--line,#cbd5e1);height:2rem;margin-bottom:0.6rem"></div>\n              <p class="ws-answer muted small" hidden><b>Teacher Key:</b> ${q.answer}</p>\n            </li>\n          `)}</ol>\n        </article>\n      ` : ""}\n    `,\n    afterRender() {\n      const printBtn = document.getElementById("ws-print-btn");\n      if (printBtn) printBtn.addEventListener("click", () => window.print());\n      const keyBtn = document.getElementById("ws-key-btn");\n      if (keyBtn) {\n        keyBtn.addEventListener("click", () => {\n          const showing = keyBtn.getAttribute("aria-expanded") === "true";\n          keyBtn.setAttribute("aria-expanded", String(!showing));\n          keyBtn.textContent = showing ? "Show Teacher Answer Key" : "Hide Teacher Answer Key";\n          document.querySelectorAll(".ws-answer").forEach((el) => {\n            el.hidden = showing;\n          });\n        });\n      }\n    },\n  };\n}\n'


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
    imp = 'import { worksheetsPage } from "./worksheets.js";\n'
    if "./worksheets.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/explore/worksheets"' not in txt:
        for anchor in ('if (path === "/glossary"', 'if (path === "/search"', 'if (path === "/ref/playbooks")', 'if (path === "/ref/equipment")'):
            if anchor in txt:
                rep = 'if (path === "/explore/worksheets") return worksheetsPage(query);\n  ' + anchor
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
    if "#/explore/worksheets" in txt:
        return False
    for anchor in ('["#/explore/glossary", "Acronym glossary"]', '["#/explore/origins", "Origin stories (75)"]', "const EXPLORE_NAV = ["):
        if anchor in txt:
            rep = anchor + ',\n  ["#/explore/worksheets", "Teacher worksheets"]' if anchor.startswith("[") else anchor + '\n  ["#/explore/worksheets", "Teacher worksheets"],'
            path.write_text(txt.replace(anchor, rep, 1), encoding="utf-8")
            return True
    return False


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_worksheets.py" in txt:
        return False
    hook = "\n# v6.1c: Native Printable Teacher Worksheets (NGSS & AP Biology)\npython3 pipeline/build_worksheets.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/worksheets"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/worksheets")\n'
        'def api_worksheets():\n'
        '    return _read_json(SITE_DIR / "data" / "worksheets.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_worksheets_py": _write_if_changed(pipe_dir / "build_worksheets.py", BUILD_WORKSHEETS_PY),
        "chem_tools_js": _write_if_changed(js_dir / "chem_tools.js", CHEM_TOOLS_JS),
        "quiz_filters_js": _write_if_changed(js_dir / "quiz_filters.js", QUIZ_FILTERS_JS),
        "worksheets_js": _write_if_changed(js_dir / "worksheets.js", WORKSHEETS_JS),
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
        (root / "site" / "data").mkdir(parents=True)

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/glossary" || path === "/ref/glossary") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const EXPLORE_NAV = [\n  ["#/explore/glossary", "Acronym glossary"]\n];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_worksheets.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_worksheets.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out["worksheets_count"] == 4, out

        ws = json.loads((root / "site" / "data" / "worksheets.json").read_text(encoding="utf-8"))
        for w in ws["worksheets"]:
            assert w["standards"] and len(w["questions"]) == 3, w
            # Ensure zero commercial links on student/teacher worksheets
            raw_txt = json.dumps(w).lower()
            for host in ("equipnet", "labx", "fedequip", "ssllc", "bookshop"):
                assert host not in raw_txt, host

        print("V61C_CHEM_QUIZ_WORKSHEETS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1c Chem Copy Tools, Quiz Filters & Teacher Worksheets patch.")
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
