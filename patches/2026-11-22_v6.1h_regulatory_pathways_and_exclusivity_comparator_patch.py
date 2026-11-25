#!/usr/bin/env python3
"""Pill by Pill v6.1h Patch: Regulatory Approval Pathways, Expedited Programs & Statutory Exclusivity Comparator (#/ref/pathways, #/explore/pathways, /api/pathways).

1. Adds `pipeline/build_pathways.py` -> `site/data/pathways.json` (5 statutory pathways,
   7 FDA/EMA expedited & rare-disease programs, 6 statutory exclusivity clocks).
2. Adds `site/js/pathways.js` (`pathwaysPage`) and wires `#/ref/pathways`, `#/explore/pathways`,
   `/api/pathways`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `pathways.json` into `pipeline/build_global_search.py`, `pipeline/build_v60_static_pages.py`
   (`/pathways/` static SEO page + sitemap entry -> 24 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-22_v6.1h_regulatory_pathways_and_exclusivity_comparator_patch.py --selftest
  python3 2026-11-22_v6.1h_regulatory_pathways_and_exclusivity_comparator_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_PATHWAYS_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1h Regulatory Pathways, Expedited Programs & Exclusivity Comparator (`site/data/pathways.json`).\n\nProvides a structured, primary-sourced side-by-side reference for:\n  1. Statutory U.S. Approval Pathways (NDA 505(b)(1), NDA 505(b)(2), ANDA 505(j), BLA 351(a), Biosimilar 351(k))\n  2. FDA & Global Expedited Programs (Fast Track, Breakthrough Therapy, Accelerated Approval, Priority Review, RMAT, Orphan Drug, EMA PRIME, PMDA Sakigake)\n  3. Statutory Exclusivity Periods (NCE 5-yr, New Clinical Investigation 3-yr, Orphan 7-yr, Reference Biologic BPCIA 12-yr, Pediatric +6-mo, GAIN +5-yr QIDP)\n\nAll legal citations are verified HTTPS official FDA / eCFR / EMA / PMDA links.\n\nUsage:\n  python3 pipeline/build_pathways.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-22"\n\nAPPROVAL_PATHWAYS = [\n    {\n        "id": "nda-505b1",\n        "name": "NDA 505(b)(1) — Full New Drug Application",\n        "statute": "FD&C Act § 505(b)(1) · 21 CFR Part 314",\n        "modality_scope": "New small molecules (NCEs) & synthetic peptides (<=40 aa)",\n        "clinical_data": "Full sponsor-owned nonclinical toxicology and Phase 1–3 clinical safety & efficacy studies.",\n        "review_clock": "10 months standard / 6 months priority (PDUFA)",\n        "exclusivity": "5 years (NCE) or 3 years (new clinical investigation)",\n        "plain": "The full, from-scratch FDA application for a brand-new chemical medicine where the company runs all its own safety and patient trials.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314",\n    },\n    {\n        "id": "nda-505b2",\n        "name": "NDA 505(b)(2) — Hybrid / Literature-Bridged NDA",\n        "statute": "FD&C Act § 505(b)(2) · 21 CFR Part 314",\n        "modality_scope": "New formulations, new routes, new combinations, or repurposed drugs",\n        "clinical_data": "Bridges to FDA\'s prior finding of safety/efficacy or published literature, supplemented by targeted PK/clinical bridging studies.",\n        "review_clock": "10 months standard / 6 months priority (PDUFA)",\n        "exclusivity": "3 years (if new clinical investigations are essential) or 5 years (if NCE)",\n        "plain": "A hybrid pathway for improving an existing medicine (such as turning an injection into a pill or extended-release tablet) without repeating every old study.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314",\n    },\n    {\n        "id": "anda-505j",\n        "name": "ANDA 505(j) — Generic Drug Application",\n        "statute": "FD&C Act § 505(j) (Hatch-Waxman) · 21 CFR Part 314",\n        "modality_scope": "Generic copies of approved small-molecule drugs",\n        "clinical_data": "No Phase 3 efficacy trials; proves pharmaceutical equivalence and bioequivalence (BE) to the Reference Listed Drug (RLD).",\n        "review_clock": "10 months standard / 8 months priority (GDUFA)",\n        "exclusivity": "180-day generic exclusivity for first Paragraph IV patent challenger",\n        "plain": "The streamlined pathway for generic pills, proving the copy contains the exact same active ingredient and enters the bloodstream at the same rate.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314",\n    },\n    {\n        "id": "bla-351a",\n        "name": "BLA 351(a) — Reference Biologic License Application",\n        "statute": "PHS Act § 351(a) · 21 CFR Part 601",\n        "modality_scope": "Monoclonal antibodies, recombinant proteins (>40 aa), vaccines, cell & gene therapies",\n        "clinical_data": "Full CMC, nonclinical, and clinical package demonstrating safety, purity, and potency.",\n        "review_clock": "10 months standard / 6 months priority (PDUFA)",\n        "exclusivity": "12 years reference biologic exclusivity (BPCIA)",\n        "plain": "The full FDA license for complex biological medicines grown in living cells—such as antibodies, vaccines, and gene therapies.",\n        "url": "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research",\n    },\n    {\n        "id": "bla-351k",\n        "name": "BLA 351(k) — Biosimilar & Interchangeable Biologic",\n        "statute": "PHS Act § 351(k) (BPCIA) · Purple Book",\n        "modality_scope": "Highly similar versions of approved reference biologics",\n        "clinical_data": "Extensive analytical similarity + PK/PD and immunogenicity studies showing no clinically meaningful differences from the reference biologic.",\n        "review_clock": "10 months (BsUFA)",\n        "exclusivity": "First interchangeable biosimilar exclusivity (12–42 months depending on litigation/launch)",\n        "plain": "The approval pathway for lower-cost \'biosimilar\' versions of complex biologic medicines, requiring rigorous structural and clinical similarity testing.",\n        "url": "https://www.fda.gov/drugs/biosimilars/biosimilar-product-information",\n    },\n]\n\nEXPEDITED_PROGRAMS = [\n    {\n        "id": "fast-track",\n        "name": "FDA Fast Track",\n        "agency": "US FDA",\n        "criteria": "Serious condition AND nonclinical or clinical data demonstrating potential to address an unmet medical need.",\n        "benefits": "More frequent FDA meetings/written guidance, eligibility for Rolling Review of eCTD sections as completed.",\n        "url": "https://www.fda.gov/patients/fast-track-breakthrough-therapy-accelerated-approval-priority-review/fast-track",\n    },\n    {\n        "id": "breakthrough",\n        "name": "FDA Breakthrough Therapy",\n        "agency": "US FDA",\n        "criteria": "Serious condition AND preliminary clinical evidence indicating substantial improvement over existing therapy on a clinically significant endpoint.",\n        "benefits": "All Fast Track features plus intensive FDA guidance from Phase 1 and senior management involvement.",\n        "url": "https://www.fda.gov/patients/fast-track-breakthrough-therapy-accelerated-approval-priority-review/breakthrough-therapy",\n    },\n    {\n        "id": "accelerated-approval",\n        "name": "FDA Accelerated Approval",\n        "agency": "US FDA",\n        "criteria": "Serious condition with unmet need; allows approval based on a surrogate or intermediate clinical endpoint reasonably likely to predict clinical benefit.",\n        "benefits": "Earlier patient access; requires mandatory post-approval confirmatory clinical trials (subject to withdrawal if benefit is not confirmed).",\n        "url": "https://www.fda.gov/patients/fast-track-breakthrough-therapy-accelerated-approval-priority-review/accelerated-approval",\n    },\n    {\n        "id": "priority-review",\n        "name": "FDA Priority Review",\n        "agency": "US FDA",\n        "criteria": "Medicine that would provide significant improvements in safety or effectiveness of treatment, diagnosis, or prevention of a serious condition.",\n        "benefits": "Shortens FDA\'s PDUFA review goal from 10 months (standard) to 6 months from filing.",\n        "url": "https://www.fda.gov/patients/fast-track-breakthrough-therapy-accelerated-approval-priority-review/priority-review",\n    },\n    {\n        "id": "orphan-drug",\n        "name": "FDA Orphan Drug Designation",\n        "agency": "US FDA",\n        "criteria": "Rare disease affecting fewer than 200,000 people in the United States (Orphan Drug Act of 1983).",\n        "benefits": "7 years of market exclusivity upon approval, clinical trial tax credits, and PDUFA application fee waiver.",\n        "url": "https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/designating-orphan-product-drugs-and-biological-products",\n    },\n    {\n        "id": "rmat",\n        "name": "FDA RMAT (Regenerative Medicine Advanced Therapy)",\n        "agency": "US FDA (CBER)",\n        "criteria": "Cell therapy, therapeutic tissue engineering, or gene therapy intended to treat a serious condition with preliminary clinical evidence of addressing unmet need.",\n        "benefits": "All Breakthrough Therapy features plus early discussions on surrogate endpoints and post-approval real-world evidence.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/cellular-gene-therapy-products/regenerative-medicine-advanced-therapy-designation",\n    },\n    {\n        "id": "ema-prime",\n        "name": "EMA PRIME (Priority Medicines)",\n        "agency": "EU EMA",\n        "criteria": "Medicines targeting an unmet medical need with early clinical data showing potential major therapeutic advantage.",\n        "benefits": "Early dedicated CHMP rapporteur, proactive scientific advice, and eligibility for Accelerated Assessment (150 vs. 210 days).",\n        "url": "https://www.ema.europa.eu/en/human-regulatory-overview/research-development/prime-priority-medicines",\n    },\n]\n\nEXCLUSIVITIES = [\n    {"type": "New Chemical Entity (NCE)", "duration": "5 years", "scope": "Small-molecule NDAs with an active moiety never previously approved by FDA.", "source": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314"},\n    {"type": "New Clinical Investigation (3-Year)", "duration": "3 years", "scope": "New indications, dosage forms, or strengths supported by new sponsor-conducted clinical trials.", "source": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314"},\n    {"type": "Orphan Drug Exclusivity (ODE)", "duration": "7 years", "scope": "Blocks FDA approval of the same drug for the same rare disease indication.", "source": "https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/designating-orphan-product-drugs-and-biological-products"},\n    {"type": "Reference Biologic Exclusivity (BPCIA)", "duration": "12 years", "scope": "Blocks biosimilar (351(k)) approval for 12 years from first licensure (filing allowed at year 4).", "source": "https://www.fda.gov/drugs/biosimilars/biosimilar-product-information"},\n    {"type": "Pediatric Exclusivity (BPCA)", "duration": "+6 months", "scope": "Adds 6 months onto existing Orange Book patents and statutory exclusivities upon completing FDA-requested pediatric studies.", "source": "https://www.fda.gov/drugs/development-resources/pediatric-product-development"},\n    {"type": "GAIN Act QIDP Exclusivity", "duration": "+5 years", "scope": "Adds 5 years to NCE/3-year/Orphan exclusivity for Qualified Infectious Disease Products targeting serious resistant pathogens.", "source": "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research"},\n]\n\n\ndef build_pathways(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "approval_pathways": APPROVAL_PATHWAYS,\n        "expedited_programs": EXPEDITED_PROGRAMS,\n        "exclusivities": EXCLUSIVITIES,\n    }\n    (data_dir / "pathways.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "approval_pathways": len(APPROVAL_PATHWAYS),\n        "expedited_programs": len(EXPEDITED_PROGRAMS),\n        "exclusivities": len(EXCLUSIVITIES),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_pathways(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
PATHWAYS_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nexport async function pathwaysPage(mode = "ref") {\n  const doc = await getJSON("data/pathways.json");\n  const paths = doc.approval_pathways || [];\n  const exp = doc.expedited_programs || [];\n  const excl = doc.exclusivities || [];\n\n  return {\n    title: "Regulatory Approval Pathways, Expedited Programs & Exclusivity Comparator",\n    body: html`\n      <h1>Regulatory Pathways, Expedited Programs &amp; Exclusivities</h1>\n      <p class="lead">${mode === "explore"\n        ? "How new pills, generics, biologics, and rare-disease medicines are reviewed by the FDA and EMA—and how long market protections last before generics arrive."\n        : "Side-by-side statutory reference comparing U.S. NDA/ANDA/BLA pathways, FDA & EMA expedited programs, and regulatory exclusivity clocks (checked " + doc.checked + ")."}</p>\n\n      <h2>1. Statutory Approval Pathways</h2>\n      <div class="tbl-wrap" tabindex="0" role="region" aria-label="Statutory approval pathways">\n        <table class="tbl"><thead><tr>\n          <th>Pathway</th><th>Statute &amp; Scope</th><th>${mode === "explore" ? "Plain-Language Summary" : "Clinical Evidence & Review Clock"}</th><th>Exclusivity</th>\n        </tr></thead>\n        <tbody>${paths.map((p) => html`<tr id="${p.id}">\n          <td><b>${p.name}</b></td>\n          <td>${p.statute}<br><span class="muted small">${p.modality_scope}</span></td>\n          <td>${mode === "explore" ? p.plain : html`${p.clinical_data}<br><span class="muted small"><b>Review clock:</b> ${p.review_clock}</span>`}</td>\n          <td>${p.exclusivity} (<a href="${p.url}" target="_blank" rel="noopener">Source</a>)</td>\n        </tr>`)}</tbody></table>\n      </div>\n\n      <h2>2. Expedited &amp; Rare-Disease Programs</h2>\n      <div class="tbl-wrap" tabindex="0" role="region" aria-label="Expedited regulatory programs">\n        <table class="tbl"><thead><tr><th>Program</th><th>Agency</th><th>Eligibility Criteria</th><th>Key Benefits</th></tr></thead>\n        <tbody>${exp.map((e) => html`<tr id="${e.id}">\n          <td><b><a href="${e.url}" target="_blank" rel="noopener">${e.name}</a></b></td>\n          <td>${e.agency}</td>\n          <td>${e.criteria}</td>\n          <td>${e.benefits}</td>\n        </tr>`)}</tbody></table>\n      </div>\n\n      <h2>3. Statutory Market Exclusivities (Separate From Patents)</h2>\n      <div class="tbl-wrap" tabindex="0" role="region" aria-label="Statutory market exclusivities">\n        <table class="tbl"><thead><tr><th>Exclusivity Type</th><th>Duration</th><th>Scope</th></tr></thead>\n        <tbody>${excl.map((x) => html`<tr>\n          <td><b><a href="${x.source}" target="_blank" rel="noopener">${x.type}</a></b></td>\n          <td><b>${x.duration}</b></td>\n          <td>${x.scope}</td>\n        </tr>`)}</tbody></table>\n      </div>\n      <p class="muted small">Related: <a href="#/ref/departments/regulatory">Stage 5: Regulatory Affairs</a> · <a href="#/ref/economics">Drug Economics &amp; LOE</a> · <a href="#/ref/ich">ICH Q1–Q12 Matrix</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { pathwaysPage } from "./pathways.js";\n'
    if "./pathways.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/pathways"' not in txt:
        for anchor in ('if (path === "/ref/classes")', 'if (path === "/explore/worksheets")', 'if (path === "/glossary"', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/pathways") return pathwaysPage("ref");\n'
                    '  if (path === "/explore/pathways") return pathwaysPage("explore");\n'
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
    if "#/ref/pathways" not in txt:
        anchor = '["#/ref/ich", "ICH Q1–Q12 matrix"]'
        if anchor in txt:
            txt = txt.replace(anchor, anchor + ',\n      ["#/ref/pathways", "Approval pathways"]', 1)
            changed = True
    if "#/explore/pathways" not in txt:
        anchor = '["#/explore/worksheets", "Teacher worksheets"]'
        if anchor in txt:
            txt = txt.replace(anchor, anchor + ',\n  ["#/explore/pathways", "Approval pathways"]', 1)
            changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_pathways.py" in txt:
        return False
    hook = "\n# v6.1h: Regulatory Pathways, Expedited Programs & Exclusivity Comparator\npython3 pipeline/build_pathways.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/pathways"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/pathways")\n'
        'def api_pathways():\n'
        '    return _read_json(SITE_DIR / "data" / "pathways.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"pathways.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    pw = _load(data_dir / "pathways.json", {}) or {}\n'
        '    for item in (pw.get("approval_pathways") or []) + (pw.get("expedited_programs") or []):\n'
        '        entries.append({\n'
        '            "kind": "pathway",\n'
        '            "group": "Glossary & Regulatory Standards",\n'
        '            "title": item.get("name", ""),\n'
        '            "summary": item.get("plain") or item.get("criteria") or "",\n'
        '            "href_ref": f"#/ref/pathways#{item.get(\'id\', \'\')}",\n'
        '            "href_explore": f"#/explore/pathways#{item.get(\'id\', \'\')}",\n'
        '            "keywords": f"{item.get(\'name\', \'\')} {item.get(\'statute\', \'\')} {item.get(\'criteria\', \'\')} {item.get(\'benefits\', \'\')} {item.get(\'exclusivity\', \'\')}".strip(),\n'
        '        })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"pathways", "#/ref/pathways"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    pw_doc = _load_json(data_dir / "pathways.json")\n'
        '    if isinstance(pw_doc, dict) and pw_doc.get("approval_pathways"):\n'
        '        pw_lis = "".join(f\'<li><b>{_esc(p["name"])}</b> ({_esc(p.get("statute",""))}) — {_esc(p.get("exclusivity",""))}</li>\' for p in pw_doc["approval_pathways"])\n'
        '        pages.append(("pathways", "#/ref/pathways", "Regulatory Approval Pathways, Expedited Programs & Exclusivities",\n'
        '                      "Compare FDA NDA 505(b)(1), 505(b)(2), ANDA 505(j), BLA 351(a), Biosimilar 351(k), Fast Track, Breakthrough Therapy, Accelerated Approval, Orphan Drug, and exclusivity clocks.",\n'
        '                      f"<ul>{pw_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/pathways"' in txt:
        return False
    anchor = '    "/#/ref/search",'
    if anchor in txt:
        path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/pathways",\n    "/#/explore/pathways",', 1), encoding="utf-8")
        return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_pathways_py": _write_if_changed(pipe_dir / "build_pathways.py", BUILD_PATHWAYS_PY),
        "pathways_js": _write_if_changed(js_dir / "pathways.js", PATHWAYS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/classes") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/ich", "ICH Q1–Q12 matrix"]] }];\nconst EXPLORE_NAV = [["#/explore/worksheets", "Teacher worksheets"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/ref/search",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_pathways.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_pathways.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out["approval_pathways"] == 5 and out["expedited_programs"] == 7 and out["exclusivities"] == 6, out

        doc = json.loads((root / "site" / "data" / "pathways.json").read_text(encoding="utf-8"))
        for p in doc["approval_pathways"]:
            assert p["url"].startswith("https://"), p
        for e in doc["expedited_programs"]:
            assert e["url"].startswith("https://"), e
        for x in doc["exclusivities"]:
            assert x["source"].startswith("https://"), x

        print("V61H_PATHWAYS_EXCLUSIVITY_COMPARATOR_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1h Regulatory Pathways & Exclusivity Comparator patch.")
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
