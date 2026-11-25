#!/usr/bin/env python3
"""Pill by Pill v6.0f Patch: Static SEO Landing Pages & Sitemap Coverage for v6.0 Routes.

Adds `pipeline/build_v60_static_pages.py` (generating crawlable static HTML pages + JSON-LD +
Open Graph metadata + `sitemap.xml` entries for `/how-drugs-are-built/`, `/departments/`,
`/departments/<id>/`, `/routes/`, `/equipment/`, and `/vendors/`) and hooks it into
`pipeline/run_all.sh` (right after `build_static_pages.py` if present).

Usage:
  python3 2026-11-21_v6.0f_static_seo_and_sitemap_patch.py --selftest
  python3 2026-11-21_v6.0f_static_seo_and_sitemap_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

BUILD_V60_STATIC_PY = '#!/usr/bin/env python3\n"""Generate crawlable static SEO landing pages & sitemap URLs for Pill by Pill v6.0 routes.\n\nReads `site/data/departments.json`, `site/data/equipment.json`, and `site/data/vendors_index.json`\n(when present) and writes real static HTML pages with canonical URLs, Open Graph / Twitter meta\ntags, Schema.org JSON-LD, plain-HTML summaries for search engines, and SPA handoff to the\ninteractive hash routes:\n  - /how-drugs-are-built/      -> #/explore/how-drugs-are-built\n  - /departments/              -> #/ref/departments\n  - /departments/<id>/         -> #/ref/departments/<id> (all 4 departments)\n  - /routes/                   -> #/ref/routes\n  - /equipment/                -> #/ref/equipment\n  - /vendors/                  -> #/ref/vendors\n\nAlso appends all generated URLs into `site/sitemap.xml` (idempotently, deduplicated).\n\nUsage:\n  python3 pipeline/build_v60_static_pages.py site/\n"""\nimport html as html_lib\nimport json\nimport pathlib\nimport re\nimport sys\nfrom datetime import date\n\n\ndef _esc(s) -> str:\n    return html_lib.escape(str(s or ""), quote=True)\n\n\ndef _load_json(path: pathlib.Path, default=None):\n    if not path.is_file():\n        return default\n    return json.loads(path.read_text(encoding="utf-8"))\n\n\ndef _render_page(*, base_url: str, rel_path: str, hash_route: str, title: str, description: str, body_html: str) -> str:\n    canonical = f"{base_url.rstrip(\'/\')}/{rel_path.strip(\'/\')}/"\n    ld = {\n        "@context": "https://schema.org",\n        "@type": "WebPage",\n        "name": title,\n        "description": description,\n        "url": canonical,\n        "isPartOf": {"@type": "WebSite", "name": "Pill by Pill", "url": base_url.rstrip("/") + "/"},\n    }\n    return (\n        "<!doctype html>\\n"\n        \'<html lang="en">\\n<head>\\n\'\n        \'  <meta charset="utf-8">\\n\'\n        \'  <meta name="viewport" content="width=device-width, initial-scale=1">\\n\'\n        f"  <title>{_esc(title)} — Pill by Pill</title>\\n"\n        f\'  <meta name="description" content="{_esc(description)}">\\n\'\n        f\'  <link rel="canonical" href="{_esc(canonical)}">\\n\'\n        f\'  <meta property="og:type" content="website">\\n\'\n        f\'  <meta property="og:title" content="{_esc(title)} — Pill by Pill">\\n\'\n        f\'  <meta property="og:description" content="{_esc(description)}">\\n\'\n        f\'  <meta property="og:url" content="{_esc(canonical)}">\\n\'\n        f\'  <meta property="og:image" content="{_esc(base_url.rstrip("/"))}/img/og-card.png">\\n\'\n        f\'  <meta name="twitter:card" content="summary_large_image">\\n\'\n        f\'  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\\n\'\n        f\'  <script>if (!/bot|crawl|spider|slurp|bingpreview/i.test(navigator.userAgent)) {{ location.replace("/{_esc(hash_route)}"); }}</script>\\n\'\n        "</head>\\n<body>\\n"\n        f"  <main>\\n    <h1>{_esc(title)}</h1>\\n"\n        f"    <p>{_esc(description)}</p>\\n"\n        f"    {body_html}\\n"\n        f\'    <p><a href="/{_esc(hash_route)}">Open interactive view in Pill by Pill</a> · <a href="/">Home</a></p>\\n\'\n        "  </main>\\n</body>\\n</html>\\n"\n    )\n\n\ndef _merge_sitemap(sitemap_path: pathlib.Path, urls: list, lastmod: str) -> int:\n    if not urls:\n        return 0\n    if sitemap_path.is_file():\n        txt = sitemap_path.read_text(encoding="utf-8")\n        existing = set(re.findall(r"<loc>([^<]+)</loc>", txt))\n        new_urls = [u for u in urls if u not in existing]\n        if not new_urls:\n            return 0\n        block = "".join(f"  <url><loc>{_esc(u)}</loc><lastmod>{lastmod}</lastmod></url>\\n" for u in new_urls)\n        if "</urlset>" in txt:\n            txt = txt.replace("</urlset>", block + "</urlset>", 1)\n        else:\n            txt += block\n        sitemap_path.write_text(txt, encoding="utf-8")\n        return len(new_urls)\n    entries = "".join(f"  <url><loc>{_esc(u)}</loc><lastmod>{lastmod}</lastmod></url>\\n" for u in urls)\n    xml = (\n        \'<?xml version="1.0" encoding="UTF-8"?>\\n\'\n        \'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\\n\'\n        + entries\n        + "</urlset>\\n"\n    )\n    sitemap_path.write_text(xml, encoding="utf-8")\n    return len(urls)\n\n\ndef build_v60_static_pages(site_dir: pathlib.Path) -> dict:\n    data_dir = site_dir / "data"\n    cfg = _load_json(site_dir / "config" / "site.json", {}) or {}\n    base_url = (cfg.get("base_url") or "https://pillbypill.netlify.app").rstrip("/")\n    lastmod = date.today().isoformat()\n\n    pages = []\n    depts_doc = _load_json(data_dir / "departments.json")\n    if depts_doc:\n        depts = depts_doc.get("departments") or []\n        routes = depts_doc.get("routes") or []\n        dept_lis = "".join(f\'<li><a href="/departments/{_esc(d["id"])}/"><b>{_esc(d["name"])}</b></a> — {_esc(d.get("plain_summary",""))}</li>\' for d in depts)\n        pages.append(("how-drugs-are-built", "#/explore/how-drugs-are-built", "How Medicines Are Built",\n                      "Plain-language guide to the four pharmaceutical development departments: Discovery, Formulation, Analytical QC, and Commercial Manufacturing.",\n                      f"<ul>{dept_lis}</ul>"))\n        pages.append(("departments", "#/ref/departments", "Pharmaceutical Encyclopedia: Departments & Workflows",\n                      "Technical reference covering Discovery, Formulation, Analytical Development & QC, and Commercial Manufacturing with FDA, ICH, and eCFR anchors.",\n                      f"<ul>{dept_lis}</ul>"))\n        for d in depts:\n            wf_lis = "".join(f\'<li><b>{_esc(w.get("step",""))}</b>: {_esc(w.get("plain",""))}</li>\' for w in (d.get("workflows") or []))\n            pages.append((f"departments/{d[\'id\']}", f"#/ref/departments/{d[\'id\']}", d["name"],\n                          d.get("plain_summary") or d.get("technical_summary") or d["name"],\n                          f"<ol>{wf_lis}</ol>"))\n        route_lis = "".join(f\'<li><b>{_esc(r["name"])}</b> — {_esc(r.get("summary",""))}</li>\' for r in routes)\n        pages.append(("routes", "#/ref/routes", "Routes of Administration & Dosage Forms",\n                      "Comparison of oral solid dosage, sterile parenteral, LNP/oligonucleotide, inhaled/pulmonary, and ophthalmic/transdermal delivery systems.",\n                      f"<ul>{route_lis}</ul>"))\n\n    equip = _load_json(data_dir / "equipment.json")\n    if isinstance(equip, list) and equip:\n        eq_lis = "".join(f\'<li><b>{_esc(e["name"])}</b> ({_esc(e.get("department",""))}) — {_esc(e.get("plain_summary",""))}</li>\' for e in equip)\n        pages.append(("equipment", "#/ref/equipment", "Pharmaceutical Equipment Market, OEMs & Lab Kits",\n                      "Reference catalog of 12 pharmaceutical R&D, QC, and manufacturing hardware classes, leading OEMs, lab kits, and public award pricing.",\n                      f"<ul>{eq_lis}</ul>"))\n\n    vendors = _load_json(data_dir / "vendors_index.json")\n    if isinstance(vendors, dict):\n        pages.append(("vendors", "#/ref/vendors", "Pharmaceutical Manufacturers, CDMOs & Site Audit Comparator",\n                      "Compare pharmaceutical manufacturing facilities and CDMOs by development stage, modality, FDA Data Dashboard inspections (NAI/VAI/OAI), Form 483s, and EMA EudraGMDP standing.",\n                      f"<p>Sites indexed: {int(vendors.get(\'count\', 0))}. {_esc(vendors.get(\'scope_note\',\'\'))}</p>"))\n\n    written_urls = []\n    for rel_path, hash_route, title, desc, body_html in pages:\n        out_fp = site_dir / rel_path / "index.html"\n        out_fp.parent.mkdir(parents=True, exist_ok=True)\n        out_fp.write_text(\n            _render_page(base_url=base_url, rel_path=rel_path, hash_route=hash_route, title=title, description=desc, body_html=body_html),\n            encoding="utf-8",\n        )\n        written_urls.append(f"{base_url}/{rel_path.strip(\'/\')}/")\n\n    sitemap_added = _merge_sitemap(site_dir / "sitemap.xml", written_urls, lastmod)\n    return {"pages_written": len(written_urls), "sitemap_urls_added": sitemap_added, "urls": written_urls}\n\n\ndef main(argv=None) -> int:\n    site_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site")\n    print(json.dumps(build_v60_static_pages(site_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_v60_static_pages.py" in txt:
        return False
    hook = "\n# v6.0f: Static SEO landing pages & sitemap entries for v6.0 routes\npython3 pipeline/build_v60_static_pages.py site\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    pipe_dir.mkdir(parents=True, exist_ok=True)
    fp = pipe_dir / "build_v60_static_pages.py"
    written = (not fp.is_file()) or (fp.read_text(encoding="utf-8") != BUILD_V60_STATIC_PY)
    if written:
        fp.write_text(BUILD_V60_STATIC_PY, encoding="utf-8")
    run_all_hooked = _patch_run_all(pipe_dir / "run_all.sh")
    return {
        "build_v60_static_pages_written": written,
        "run_all_sh_hooked": run_all_hooked,
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "data").mkdir(parents=True)
        (root / "site" / "config").mkdir(parents=True)
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\npython3 pipeline/build_static_pages.py site\n", encoding="utf-8")
        (root / "site" / "config" / "site.json").write_text('{"base_url": "https://pillbypill.netlify.app"}\n', encoding="utf-8")
        (root / "site" / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            '  <url><loc>https://pillbypill.netlify.app/</loc></url>\n</urlset>\n',
            encoding="utf-8",
        )
        (root / "site" / "data" / "departments.json").write_text(json.dumps({
            "departments": [
                {"id": "discovery", "name": "Discovery", "plain_summary": "Early R&D", "workflows": [{"step": "1", "plain": "HTS"}]},
                {"id": "formulation", "name": "Formulation", "plain_summary": "Dosage forms", "workflows": [{"step": "1", "plain": "OSD"}]},
                {"id": "analytical", "name": "Analytical QC", "plain_summary": "Testing", "workflows": [{"step": "1", "plain": "HPLC"}]},
                {"id": "manufacturing", "name": "Manufacturing", "plain_summary": "Scale-up", "workflows": [{"step": "1", "plain": "cGMP"}]},
            ],
            "routes": [{"id": "oral-solid", "name": "Oral Solid Dosage", "summary": "Tablets & capsules"}],
        }), encoding="utf-8")
        (root / "site" / "data" / "equipment.json").write_text(json.dumps([
            {"id": "eq-hplc-uplc", "name": "HPLC / UPLC", "department": "analytical", "plain_summary": "Purity testing"}
        ]), encoding="utf-8")
        (root / "site" / "data" / "vendors_index.json").write_text(json.dumps({"count": 0, "scope_note": "21 CFR 314.430 disclosure."}), encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        out1 = json.loads(subprocess.check_output([sys.executable, str(root / "pipeline" / "build_v60_static_pages.py"), str(root / "site")], text=True))
        assert out1["pages_written"] == 9 and out1["sitemap_urls_added"] == 9, out1
        # Sitemap idempotency check
        out2 = json.loads(subprocess.check_output([sys.executable, str(root / "pipeline" / "build_v60_static_pages.py"), str(root / "site")], text=True))
        assert out2["sitemap_urls_added"] == 0, out2

        html_text = (root / "site" / "departments" / "formulation" / "index.html").read_text(encoding="utf-8")
        assert 'application/ld+json' in html_text and '#/ref/departments/formulation' in html_text
        print("V60F_STATIC_SEO_AND_SITEMAP_SELFTEST_PASSED", json.dumps(out1, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.0f Static SEO & Sitemap patch.")
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
