#!/usr/bin/env python3
"""Pill by Pill v6.1g Patch: Complete v6.1 Static SEO & Sitemap Coverage (+10 Landing Pages), Full Global Search Indexing & v6.1 Browser/WCAG Route Coverage.

1. Expands `pipeline/build_v60_static_pages.py` to generate 10 additional crawlable static
   HTML landing pages + JSON-LD + `sitemap.xml` entries (`/software/`, `/economics/`,
   `/partners/`, `/playbooks/`, `/origins/`, `/glossary/`, `/trace/`, `/ich/`, `/worksheets/`,
   `/classes/`), bringing total encyclopedia static SEO landing pages to 23.
2. Expands `pipeline/build_global_search.py` to index all 24 Acronym Glossary terms, 11 ICH
   Q1–Q12 guidelines, 5 Trace-One-Drug Storyboards, 4 Printable Teacher Worksheets, and 14
   WHO ATC Level-1 therapeutic classes.
3. Expands `tests/test_v60_site.py` so headless Chromium + axe-core WCAG 2.2 AA browser
   testing covers all new v6.1 routes across desktop, phone, and dark mode.

Usage:
  python3 2026-11-22_v6.1g_seo_global_search_and_browser_test_coverage_patch.py --selftest
  python3 2026-11-22_v6.1g_seo_global_search_and_browser_test_coverage_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

V61_STATIC_PAGES_SNIPPET = '\n    # v6.1g: Static SEO landing pages & sitemap coverage for v6.0j–v6.1f routes\n    sw_doc = _load_json(data_dir / "software_stack.json")\n    if isinstance(sw_doc, dict) and sw_doc.get("items"):\n        sw_lis = "".join(f\'<li><b>{_esc(s["name"])}</b> — {_esc(s.get("plain_summary",""))}</li>\' for s in sw_doc["items"])\n        pages.append(("software", "#/ref/software", "Enterprise Pharma Software & Informatics Stack",\n                      "10 regulated pharmaceutical software categories (ELN, LIMS, CDS, EDC, CTMS/eTMF, RIM/eCTD, QMS, MES/eBR, Pharmacovigilance, DSCSA) mapped to 21 CFR Part 11.",\n                      f"<ul>{sw_lis}</ul>"))\n\n    ec_doc = _load_json(data_dir / "economics.json")\n    if isinstance(ec_doc, dict) and ec_doc.get("capital_formation"):\n        ec_lis = "".join(f\'<li><b>{_esc(c["stage"])}</b> ({_esc(c.get("primary_funders",""))}) — {_esc(c.get("plain",""))}</li>\' for c in ec_doc["capital_formation"])\n        pages.append(("economics", "#/ref/economics", "Drug Development Economics, Capital Formation & Pricing",\n                      "Primary-sourced breakdown of pharmaceutical capital formation, CBO/JAMA R&D cost benchmarks, and the commercial Gross-to-Net (GTN) payer waterfall.",\n                      f"<ol>{ec_lis}</ol>"))\n\n    pt_doc = _load_json(data_dir / "partners.json")\n    if isinstance(pt_doc, dict) and pt_doc.get("categories"):\n        pt_lis = "".join(f\'<li><b>{_esc(c["name"])}</b> — {_esc(c.get("plain_summary",""))}</li>\' for c in pt_doc["categories"])\n        pages.append(("partners", "#/ref/partners", "Pharma Execution Partner Ecosystem (CROs, Labs, 3PLs & Specialty)",\n                      "6 specialized partner sectors executing preclinical GLP, clinical trials, central labs, cold-chain 3PL logistics, wholesale distribution, and REMS specialty pharmacy.",\n                      f"<ul>{pt_lis}</ul>"))\n\n    pb_doc = _load_json(data_dir / "playbooks.json")\n    if isinstance(pb_doc, dict) and pb_doc.get("modalities"):\n        pb_lis = "".join(f\'<li><b>{_esc(m["name"])}</b> ({_esc(m.get("mw_range",""))}) — {_esc(m.get("plain_summary",""))}</li>\' for m in pb_doc["modalities"])\n        pages.append(("playbooks", "#/ref/playbooks", "Modality Playbooks: 5 Medicine Types Across 8 Lifecycle Stages",\n                      "Side-by-side comparison of Small Molecules, Monoclonal Antibodies, Therapeutic Peptides, Oligonucleotides/mRNA-LNP, and Cell & Gene Therapies.",\n                      f"<ul>{pb_lis}</ul>"))\n\n    og_doc = _load_json(data_dir / "origins_gallery.json")\n    if isinstance(og_doc, dict) and og_doc.get("stories"):\n        pages.append(("origins", "#/explore/origins", f"Discovery Origin Stories ({len(og_doc[\'stories\'])} Landmark Medicines)",\n                      "Browse primary-sourced discovery stories of landmark medicines from natural products and accidental breakthroughs to rational structure-based design.",\n                      f"<p>{len(og_doc[\'stories\'])} verified discovery origin stories indexed across {len(og_doc.get(\'categories\') or [])} categories.</p>"))\n\n    gl_doc = _load_json(data_dir / "glossary.json")\n    if isinstance(gl_doc, dict) and gl_doc.get("terms"):\n        gl_lis = "".join(f\'<li><b>{_esc(t["term"])}</b> ({_esc(t.get("full",""))}) — {_esc(t.get("plain",""))}</li>\' for t in gl_doc["terms"][:24])\n        pages.append(("glossary", "#/ref/glossary", "Pharmaceutical & Regulatory Acronym Glossary",\n                      "Plain-language and technical definitions for essential pharma, FDA/EMA regulatory, cGMP, and pricing acronyms (IND, NDA, BLA, cGMP, FEI, WAC, PBM, DSCSA, LNP).",\n                      f"<ul>{gl_lis}</ul>"))\n\n    tr_doc = _load_json(data_dir / "trace_storyboards.json")\n    if isinstance(tr_doc, dict) and tr_doc.get("storyboards"):\n        tr_lis = "".join(f\'<li><b>{_esc(s["drug_name"])}</b> ({_esc(s.get("modality",""))}) — {_esc(s.get("headline",""))}</li>\' for s in tr_doc["storyboards"])\n        pages.append(("trace", "#/explore/trace", "Trace One Drug End-to-End (Idea to Pharmacy)",\n                      "Step-by-step 8-stage storyboards tracing flagship medicines across all 5 modalities from early discovery to commercial distribution.",\n                      f"<ul>{tr_lis}</ul>"))\n\n    ich_doc = _load_json(data_dir / "ich_matrix.json")\n    if isinstance(ich_doc, dict) and ich_doc.get("guidelines"):\n        ich_lis = "".join(f\'<li><b>{_esc(g["code"])}</b> — {_esc(g.get("title",""))}</li>\' for g in ich_doc["guidelines"])\n        pages.append(("ich", "#/ref/ich", "ICH Q1–Q12 Quality Guidelines Quick-Reference Matrix",\n                      "Quick-reference map of International Council for Harmonisation (ICH) Quality guidelines for stability, analytical validation, impurities, biologics, QbD, and cGMP.",\n                      f"<ul>{ich_lis}</ul>"))\n\n    ws_doc = _load_json(data_dir / "worksheets.json")\n    if isinstance(ws_doc, dict) and ws_doc.get("worksheets"):\n        ws_lis = "".join(f\'<li><b>{_esc(w["title"])}</b> ({_esc(w.get("grade_band",""))})</li>\' for w in ws_doc["worksheets"])\n        pages.append(("worksheets", "#/explore/worksheets", "Printable Classroom Worksheets (NGSS & AP Biology)",\n                      "Free, ad-free printable classroom worksheets aligned to NGSS and AP Biology with toggleable Teacher Answer Keys.",\n                      f"<ul>{ws_lis}</ul>"))\n\n    atc_doc = _load_json(data_dir / "atc_tree.json")\n    if isinstance(atc_doc, dict) and atc_doc.get("groups"):\n        atc_lis = "".join(f\'<li><b>{_esc(g["code"])}</b> — {_esc(g.get("name",""))} ({int(g.get("count",0))} medicines)</li>\' for g in atc_doc["groups"])\n        pages.append(("classes", "#/ref/classes", "WHO ATC Therapeutic Class Tree",\n                      "Browse approved medicines across the 14 official WHO Anatomical Therapeutic Chemical (ATC) organ systems and therapeutic subgroups.",\n                      f"<ul>{atc_lis}</ul>"))\n'
V61_GLOBAL_SEARCH_SNIPPET = '\n    # v6.1g: Index Acronym Glossary, ICH Q1–Q12 Matrix, Trace Storyboards, Worksheets & ATC Classes\n    glossary = _load(data_dir / "glossary.json", {}) or {}\n    for t in glossary.get("terms") or []:\n        entries.append({\n            "kind": "glossary",\n            "group": "Glossary & Regulatory Standards",\n            "title": f"{t.get(\'term\', \'\')} — {t.get(\'full\', \'\')}",\n            "summary": t.get("plain", ""),\n            "href_ref": f"#/ref/glossary?q={t.get(\'term\', \'\')}",\n            "href_explore": f"#/explore/glossary?q={t.get(\'term\', \'\')}",\n            "keywords": f"{t.get(\'term\', \'\')} {t.get(\'full\', \'\')} {t.get(\'category\', \'\')} {t.get(\'plain\', \'\')} {t.get(\'technical\', \'\')}".strip(),\n        })\n\n    ich = _load(data_dir / "ich_matrix.json", {}) or {}\n    for g in ich.get("guidelines") or []:\n        entries.append({\n            "kind": "ich",\n            "group": "Glossary & Regulatory Standards",\n            "title": f"{g.get(\'code\', \'\')}: {g.get(\'title\', \'\')}",\n            "summary": g.get("summary", ""),\n            "href_ref": "#/ref/ich",\n            "href_explore": "#/ref/ich",\n            "keywords": f"{g.get(\'code\', \'\')} {g.get(\'title\', \'\')} {g.get(\'stage\', \'\')} {g.get(\'summary\', \'\')}".strip(),\n        })\n\n    traces = _load(data_dir / "trace_storyboards.json", {}) or {}\n    for s in traces.get("storyboards") or []:\n        st_txt = " ".join(x.get("summary", "") for x in (s.get("stages") or []))\n        entries.append({\n            "kind": "trace",\n            "group": "End-to-End Drug Storyboards",\n            "title": f"Trace End-to-End: {s.get(\'drug_name\', \'\')} ({s.get(\'modality\', \'\')})",\n            "summary": s.get("headline", ""),\n            "href_ref": f"#/ref/trace?drug={s.get(\'id\', \'\')}",\n            "href_explore": f"#/explore/trace?drug={s.get(\'id\', \'\')}",\n            "keywords": f"{s.get(\'drug_name\', \'\')} {s.get(\'modality\', \'\')} {s.get(\'headline\', \'\')} {st_txt}".strip(),\n        })\n\n    ws = _load(data_dir / "worksheets.json", {}) or {}\n    for w in ws.get("worksheets") or []:\n        entries.append({\n            "kind": "worksheet",\n            "group": "Classroom & Worksheets",\n            "title": w.get("title", ""),\n            "summary": f"{w.get(\'grade_band\', \'\')} · {\', \'.join(w.get(\'standards\') or [])}",\n            "href_ref": f"#/explore/worksheets?id={w.get(\'id\', \'\')}",\n            "href_explore": f"#/explore/worksheets?id={w.get(\'id\', \'\')}",\n            "keywords": f"worksheet teacher classroom NGSS AP Biology {w.get(\'title\', \'\')} {\' \'.join(w.get(\'standards\') or [])}".strip(),\n        })\n\n    atc = _load(data_dir / "atc_tree.json", {}) or {}\n    for g in atc.get("groups") or []:\n        entries.append({\n            "kind": "atc",\n            "group": "Therapeutic Classes (WHO ATC)",\n            "title": f"ATC {g.get(\'code\', \'\')} — {g.get(\'name\', \'\')}",\n            "summary": f"{g.get(\'count\', 0)} tagged medicines across {len(g.get(\'subgroups\') or [])} therapeutic subgroups.",\n            "href_ref": f"#/ref/classes?group={g.get(\'code\', \'\')}",\n            "href_explore": f"#/ref/classes?group={g.get(\'code\', \'\')}",\n            "keywords": f"ATC {g.get(\'code\', \'\')} {g.get(\'name\', \'\')} therapeutic class".strip(),\n        })\n'


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"software", "#/ref/software"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    path.write_text(txt.replace(anchor, V61_STATIC_PAGES_SNIPPET.lstrip("\n") + "\n" + anchor, 1), encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"Glossary & Regulatory Standards"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    path.write_text(txt.replace(anchor, V61_GLOBAL_SEARCH_SNIPPET.lstrip("\n") + "\n" + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/classes"' in txt:
        return False
    anchor = '    "/#/ref/vendors?view=parents",'
    extra = (
        '    "/#/ref/vendors?view=parents",\n'
        '    "/#/ref/software",\n'
        '    "/#/ref/economics",\n'
        '    "/#/explore/economics",\n'
        '    "/#/ref/partners",\n'
        '    "/#/ref/playbooks",\n'
        '    "/#/explore/origins",\n'
        '    "/#/ref/glossary",\n'
        '    "/#/explore/trace",\n'
        '    "/#/ref/ich",\n'
        '    "/#/explore/worksheets",\n'
        '    "/#/ref/classes",\n'
        '    "/#/ref/search",'
    )
    if anchor in txt:
        path.write_text(txt.replace(anchor, extra, 1), encoding="utf-8")
        return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    return {
        "static_seo_v61_10pages_added": _patch_static_pages(root / "pipeline" / "build_v60_static_pages.py"),
        "global_search_v61_indexed": _patch_global_search(root / "pipeline" / "build_global_search.py"),
        "test_v60_site_v61_routes_added": _patch_test_v60_site(root / "tests" / "test_v60_site.py"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "data").mkdir(parents=True)
        (root / "tests").mkdir()

        # Minimal fixtures matching real anchors
        (root / "pipeline" / "build_v60_static_pages.py").write_text(
            'import html as html_lib, json, pathlib, sys\n'
            'def _esc(s): return html_lib.escape(str(s or ""), quote=True)\n'
            'def _load_json(p, d=None): return json.loads(p.read_text("utf-8")) if p.is_file() else d\n'
            'def build_v60_static_pages(site_dir):\n'
            '    data_dir = site_dir / "data"\n'
            '    pages = []\n'
            '    written_urls = []\n'
            '    return {"pages_count": len(pages)}\n'
            'if __name__ == "__main__": print(json.dumps(build_v60_static_pages(pathlib.Path(sys.argv[1]))))\n',
            encoding="utf-8",
        )
        (root / "pipeline" / "build_global_search.py").write_text(
            'import json, pathlib, sys\nCHECKED = "2026-11-22"\n'
            'def _load(p, d=None): return json.loads(p.read_text("utf-8")) if p.is_file() else d\n'
            'def build_global_search(data_dir):\n'
            '    entries = []\n'
            '    payload = {"checked": CHECKED, "count": len(entries), "entries": entries}\n'
            '    (data_dir / "global_search.json").write_text(json.dumps(payload), encoding="utf-8")\n'
            '    return {"global_search_entries": len(entries)}\n'
            'if __name__ == "__main__": print(json.dumps(build_global_search(pathlib.Path(sys.argv[1]))))\n',
            encoding="utf-8",
        )
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/ref/vendors?view=parents",\n]\n', encoding="utf-8")

        # Seed all 10 v6.1 data files
        dd = root / "site" / "data"
        (dd / "software_stack.json").write_text(json.dumps({"items": [{"name": "LIMS", "plain_summary": "Lab tracking"}]}), encoding="utf-8")
        (dd / "economics.json").write_text(json.dumps({"capital_formation": [{"stage": "1", "primary_funders": "NIH", "plain": "Grants"}]}), encoding="utf-8")
        (dd / "partners.json").write_text(json.dumps({"categories": [{"name": "CROs", "plain_summary": "Trials"}]}), encoding="utf-8")
        (dd / "playbooks.json").write_text(json.dumps({"modalities": [{"name": "mAb", "mw_range": "150kDa", "plain_summary": "Antibody"}]}), encoding="utf-8")
        (dd / "origins_gallery.json").write_text(json.dumps({"stories": [{"medicine": "ASPIRIN"}], "categories": [{"name": "Natural"}]}), encoding="utf-8")
        (dd / "glossary.json").write_text(json.dumps({"terms": [{"term": "IND", "full": "Investigational New Drug", "category": "Reg", "plain": "Permit", "technical": "21 CFR 312"}]}), encoding="utf-8")
        (dd / "trace_storyboards.json").write_text(json.dumps({"storyboards": [{"id": "imatinib", "drug_name": "Imatinib", "modality": "Small Molecule", "headline": "CML", "stages": [{"summary": "BCR-ABL"}]}]}), encoding="utf-8")
        (dd / "ich_matrix.json").write_text(json.dumps({"guidelines": [{"code": "ICH Q2", "title": "Validation", "stage": "QC", "summary": "Methods"}]}), encoding="utf-8")
        (dd / "worksheets.json").write_text(json.dumps({"worksheets": [{"id": "ws-1", "title": "WS 1", "grade_band": "9-12", "standards": ["NGSS"]}]}), encoding="utf-8")
        (dd / "atc_tree.json").write_text(json.dumps({"groups": [{"code": "C", "name": "Cardiovascular", "count": 10, "subgroups": []}]}), encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        sp_out = json.loads(subprocess.check_output([sys.executable, str(root / "pipeline" / "build_v60_static_pages.py"), str(root / "site")], text=True))
        assert sp_out["pages_count"] == 10, sp_out

        gs_out = json.loads(subprocess.check_output([sys.executable, str(root / "pipeline" / "build_global_search.py"), str(dd)], text=True))
        assert gs_out["global_search_entries"] == 5, gs_out

        print("V61G_SEO_SEARCH_BROWSER_COVERAGE_SELFTEST_PASSED", json.dumps({**sp_out, **gs_out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1g Static SEO, Global Search & Browser Test Coverage patch.")
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
