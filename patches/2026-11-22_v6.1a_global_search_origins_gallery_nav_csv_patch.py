#!/usr/bin/env python3
"""Pill by Pill v6.1a Patch: Unified Global Search, 75-Origin-Stories Gallery, Explore Hub v6.0 Links & CSV Table Export.

Implements the top P1 UX gaps identified in the 2026-11-21 Blind 6-Role Audit:
  1. Unified Global Search (`pipeline/build_global_search.py` -> `site/data/global_search.json`,
     `site/js/global_search.js`, `#/search`, `#/ref/search`, `#/explore/search`, `/api/search`).
  2. 75-Origin-Stories Gallery (`pipeline/build_origins_gallery.py` -> `site/data/origins_gallery.json`,
     `site/js/origins.js`, `#/explore/origins`) with category filters and Random Story button.
  3. Zero-dependency CSV Table Export (`site/js/csv_export.js`) wired into `site/js/vendors.js`
     and `site/js/equipment.js` for industry & regulatory professionals.
  4. Navigation & Explore Hub wiring in `site/js/app.js`, `site/js/layout.js`, `pipeline/run_all.sh`,
     and `app.py`.

Usage:
  python3 2026-11-22_v6.1a_global_search_origins_gallery_nav_csv_patch.py --selftest
  python3 2026-11-22_v6.1a_global_search_origins_gallery_nav_csv_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_GLOBAL_SEARCH_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1a Unified Global Search index (`site/data/global_search.json`).\n\nAggregates searchable records across all v6.0 encyclopedia modules so users can search\nhardware ("HPLC", "lyophilizer"), software ("21 CFR Part 11", "LIMS"), lifecycle stages\n("Phase 2", "IND"), economics ("PBM rebate", "WAC"), partner sectors ("CRO", "3PL"),\nmodality playbooks ("CAR-T", "mAb"), routes of administration, and origin stories from\none unified search bar alongside `drug_index.json`.\n\nUsage:\n  python3 pipeline/build_global_search.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-22"\n\n\ndef _load(path: pathlib.Path, default=None):\n    if not path.is_file():\n        return default\n    return json.loads(path.read_text(encoding="utf-8"))\n\n\ndef build_global_search(data_dir: pathlib.Path) -> dict:\n    entries = []\n\n    depts_doc = _load(data_dir / "departments.json", {}) or {}\n    for d in depts_doc.get("departments") or []:\n        wf_text = " ".join(\n            f"{w.get(\'step\', \'\')} {w.get(\'plain\', \'\')} {w.get(\'expert\', \'\') or w.get(\'technical\', \'\')}"\n            for w in (d.get("workflows") or [])\n        )\n        entries.append({\n            "kind": "department",\n            "group": "Lifecycle & Encyclopedia",\n            "title": d.get("name", d.get("id", "")),\n            "summary": d.get("plain_summary", ""),\n            "href_ref": f"#/ref/departments/{d[\'id\']}",\n            "href_explore": f"#/explore/departments/{d[\'id\']}",\n            "keywords": f"{d.get(\'id\', \'\')} {d.get(\'name\', \'\')} {d.get(\'plain_summary\', \'\')} {d.get(\'technical_summary\', \'\')} {wf_text}".strip(),\n        })\n    for r in depts_doc.get("routes") or []:\n        entries.append({\n            "kind": "route",\n            "group": "Lifecycle & Encyclopedia",\n            "title": r.get("name", r.get("id", "")),\n            "summary": r.get("summary", ""),\n            "href_ref": f"#/ref/routes#{r[\'id\']}",\n            "href_explore": "#/explore/departments/formulation",\n            "keywords": f"{r.get(\'id\', \'\')} {r.get(\'name\', \'\')} {r.get(\'summary\', \'\')} {\' \'.join(r.get(\'cqas\') or [])}".strip(),\n        })\n\n    equip = _load(data_dir / "equipment.json", [])\n    if isinstance(equip, list):\n        for e in equip:\n            oems = ", ".join(o.get("name", "") for o in (e.get("leading_oems") or []))\n            spec = e.get("technical_spec") or {}\n            entries.append({\n                "kind": "equipment",\n                "group": "Equipment & Software",\n                "title": e.get("name", e.get("id", "")),\n                "summary": e.get("plain_summary", ""),\n                "href_ref": f"#/ref/equipment#{e[\'id\']}",\n                "href_explore": f"#/explore/departments/{e.get(\'department\', \'formulation\')}",\n                "keywords": f"{e.get(\'id\', \'\')} {e.get(\'name\', \'\')} {e.get(\'department\', \'\')} {oems} {spec.get(\'primary_use\', \'\')} {spec.get(\'gmp_compliance\', \'\')}".strip(),\n            })\n\n    sw_doc = _load(data_dir / "software_stack.json", {}) or {}\n    for s in sw_doc.get("items") or []:\n        entries.append({\n            "kind": "software",\n            "group": "Equipment & Software",\n            "title": s.get("name", s.get("id", "")),\n            "summary": s.get("plain_summary", ""),\n            "href_ref": f"#/ref/software#{s[\'id\']}",\n            "href_explore": "#/explore/how-drugs-are-built",\n            "keywords": f"{s.get(\'id\', \'\')} {s.get(\'name\', \'\')} {s.get(\'technical_spec\', \'\')} {s.get(\'compliance\', \'\')} {\' \'.join(s.get(\'leading_vendors\') or [])}".strip(),\n        })\n\n    econ = _load(data_dir / "economics.json", {}) or {}\n    for c in econ.get("capital_formation") or []:\n        entries.append({\n            "kind": "economics",\n            "group": "Economics, Partners & Playbooks",\n            "title": f"Capital Formation: {c.get(\'stage\', \'\')}",\n            "summary": c.get("plain", ""),\n            "href_ref": "#/ref/economics",\n            "href_explore": "#/explore/economics",\n            "keywords": f"{c.get(\'stage\', \'\')} {c.get(\'primary_funders\', \'\')} {c.get(\'plain\', \'\')} {c.get(\'technical\', \'\')}".strip(),\n        })\n    for g in econ.get("gross_to_net_waterfall") or []:\n        entries.append({\n            "kind": "economics",\n            "group": "Economics, Partners & Playbooks",\n            "title": f"Gross-to-Net: {g.get(\'step\', \'\')}",\n            "summary": g.get("role", ""),\n            "href_ref": "#/ref/economics",\n            "href_explore": "#/explore/economics",\n            "keywords": f"gross to net GTN pricing {g.get(\'step\', \'\')} {g.get(\'role\', \'\')}".strip(),\n        })\n\n    partners = _load(data_dir / "partners.json", {}) or {}\n    for p in partners.get("categories") or []:\n        entries.append({\n            "kind": "partner",\n            "group": "Economics, Partners & Playbooks",\n            "title": p.get("name", p.get("id", "")),\n            "summary": p.get("plain_summary", ""),\n            "href_ref": f"#/ref/partners#{p[\'id\']}",\n            "href_explore": "#/explore/partners",\n            "keywords": f"{p.get(\'id\', \'\')} {p.get(\'name\', \'\')} {p.get(\'technical_scope\', \'\')} {p.get(\'regulatory_framework\', \'\')} {\' \'.join(p.get(\'major_players\') or [])}".strip(),\n        })\n\n    playbooks = _load(data_dir / "playbooks.json", {}) or {}\n    for m in playbooks.get("modalities") or []:\n        st_txt = " ".join((m.get("stages") or {}).values())\n        entries.append({\n            "kind": "playbook",\n            "group": "Economics, Partners & Playbooks",\n            "title": f"Modality Playbook: {m.get(\'name\', \'\')}",\n            "summary": m.get("plain_summary", ""),\n            "href_ref": "#/ref/playbooks",\n            "href_explore": "#/explore/playbooks",\n            "keywords": f"{m.get(\'id\', \'\')} {m.get(\'name\', \'\')} {m.get(\'mw_range\', \'\')} {st_txt}".strip(),\n        })\n\n    origins = _load(data_dir / "origins_gallery.json", {}) or {}\n    for o in origins.get("stories") or []:\n        entries.append({\n            "kind": "origin",\n            "group": "Discovery Origin Stories",\n            "title": f"Origin Story: {o.get(\'medicine\', \'\')}",\n            "summary": o.get("simple", ""),\n            "href_ref": f"#/explore/origins?q={o.get(\'medicine\', \'\')}",\n            "href_explore": f"#/explore/origins?q={o.get(\'medicine\', \'\')}",\n            "keywords": f"{o.get(\'medicine\', \'\')} {o.get(\'category\', \'\')} {o.get(\'simple\', \'\')} {o.get(\'expert\', \'\')}".strip(),\n        })\n\n    payload = {"checked": CHECKED, "count": len(entries), "entries": entries}\n    data_dir.mkdir(parents=True, exist_ok=True)\n    (data_dir / "global_search.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {"global_search_entries": len(entries)}\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_global_search(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
BUILD_ORIGINS_GALLERY_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1a Browsable Origin Stories Gallery (`site/data/origins_gallery.json`).\n\nReads `pipeline/origin_stories.json` (75 primary-sourced discovery stories) and emits a\nfrontend-ready gallery index grouped by discovery category (Accidental, Natural Product,\nRational Design, Semi-synthetic, Biologic/Genetic, etc.) with slug links to each medicine page.\n\nUsage:\n  python3 pipeline/build_origins_gallery.py pipeline/origin_stories.json site/data\n"""\nimport json\nimport pathlib\nimport re\nimport sys\n\nCHECKED = "2026-11-22"\n\n\ndef _slug(name: str) -> str:\n    return re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")\n\n\ndef build_origins_gallery(origin_json: pathlib.Path, data_dir: pathlib.Path) -> dict:\n    if not origin_json.is_file():\n        stories = []\n    else:\n        raw = json.loads(origin_json.read_text(encoding="utf-8"))\n        stories = raw.get("stories") if isinstance(raw, dict) else raw\n        if not isinstance(stories, list):\n            stories = []\n\n    categories = {}\n    out_stories = []\n    for s in stories:\n        med = str(s.get("medicine") or "").strip()\n        if not med:\n            continue\n        cat = str(s.get("category") or "Other").strip()\n        categories[cat] = categories.get(cat, 0) + 1\n        out_stories.append({\n            "medicine": med,\n            "slug": _slug(med),\n            "category": cat,\n            "simple": s.get("simple", ""),\n            "expert": s.get("expert", ""),\n            "sources": s.get("sources") or [],\n            "checked": s.get("checked", CHECKED),\n        })\n\n    out_stories.sort(key=lambda x: x["medicine"])\n    payload = {\n        "checked": CHECKED,\n        "count": len(out_stories),\n        "categories": [{"name": k, "count": v} for k, v in sorted(categories.items(), key=lambda kv: (-kv[1], kv[0]))],\n        "stories": out_stories,\n    }\n    data_dir.mkdir(parents=True, exist_ok=True)\n    (data_dir / "origins_gallery.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {"origins_gallery_stories": len(out_stories), "categories": len(categories)}\n\n\ndef main(argv=None) -> int:\n    origin_json = pathlib.Path(argv[0]) if argv and len(argv) >= 1 else pathlib.Path("pipeline/origin_stories.json")\n    data_dir = pathlib.Path(argv[1]) if argv and len(argv) >= 2 else pathlib.Path("site/data")\n    print(json.dumps(build_origins_gallery(origin_json, data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
CSV_EXPORT_JS = 'export function csvEscape(val) {\n  const s = val == null ? "" : String(val);\n  if (/[",\\r\\n]/.test(s)) return \'"\' + s.replace(/"/g, \'""\') + \'"\';\n  return s;\n}\n\nexport function rowsToCsv(columns, rows) {\n  const header = columns.map((c) => csvEscape(c.label)).join(",");\n  const lines = rows.map((r) => columns.map((c) => csvEscape(typeof c.get === "function" ? c.get(r) : r[c.key])).join(","));\n  return [header, ...lines].join("\\r\\n") + "\\r\\n";\n}\n\nexport function downloadCsv(filename, columns, rows) {\n  const csv = rowsToCsv(columns, rows);\n  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });\n  const url = URL.createObjectURL(blob);\n  const a = document.createElement("a");\n  a.href = url;\n  a.download = filename;\n  document.body.appendChild(a);\n  a.click();\n  a.remove();\n  setTimeout(() => URL.revokeObjectURL(url), 1000);\n}\n'
GLOBAL_SEARCH_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nexport async function globalSearchPage(query, mode = "ref") {\n  const q = ((query && query.get("q")) || "").trim();\n  const ql = q.toLowerCase();\n  const gs = await getJSON("data/global_search.json").catch(() => ({ entries: [] }));\n  const entries = gs.entries || [];\n\n  let drugMatches = [];\n  if (ql.length >= 2) {\n    const idx = await getJSON("data/drug_index.json").catch(() => null);\n    const rows = Array.isArray(idx) ? idx : (idx && idx.rows) || [];\n    for (const r of rows) {\n      const name = String(r.n || r.name || r.id || "");\n      const id = String(r.i || r.id || "");\n      if (name.toLowerCase().includes(ql) || id.toLowerCase().includes(ql)) {\n        drugMatches.push({ id, name, year: r.y || r.first_year || "" });\n        if (drugMatches.length >= 25) break;\n      }\n    }\n  }\n\n  const encMatches = ql.length >= 2\n    ? entries.filter((e) => `${e.title} ${e.summary} ${e.keywords}`.toLowerCase().includes(ql)).slice(0, 60)\n    : [];\n\n  const grouped = new Map();\n  for (const m of encMatches) {\n    if (!grouped.has(m.group)) grouped.set(m.group, []);\n    grouped.get(m.group).push(m);\n  }\n\n  const baseRoute = mode === "explore" ? "#/explore/search" : "#/ref/search";\n  const drugBase = mode === "explore" ? "#/explore/medicine/" : "#/ref/drug/";\n\n  return {\n    title: q ? `Search: ${q}` : "Unified Global Search",\n    body: html`\n      <h1>Unified Global Search</h1>\n      <p class="lead">Search across approved medicines, all 8 lifecycle stages, 18 hardware classes, 10 software systems, drug economics, partner sectors, modality playbooks, and 75 discovery origin stories.</p>\n      <form id="gs-form" class="filters" role="search" aria-label="Global Pill by Pill search">\n        <label for="gs-input">Search everything</label>\n        <input id="gs-input" type="search" value="${q}" placeholder="Try: HPLC, Phase 2, 21 CFR Part 11, PBM rebate, CRO, CAR-T, aspirin...">\n        <button type="submit">Search</button>\n      </form>\n      ${ql.length < 2 ? html`\n        <p class="muted">Type at least 2 characters to search ${entries.length} encyclopedia records plus the full medicine catalogue.</p>\n        <p class="small">Quick examples:\n          <a href="${baseRoute}?q=HPLC">HPLC</a> ·\n          <a href="${baseRoute}?q=21%20CFR%20Part%2011">21 CFR Part 11</a> ·\n          <a href="${baseRoute}?q=PBM">PBM rebates</a> ·\n          <a href="${baseRoute}?q=CRO">CROs</a> ·\n          <a href="${baseRoute}?q=LNP">LNP</a> ·\n          <a href="${baseRoute}?q=CAR-T">CAR-T</a>\n        </p>\n      ` : html`\n        <p class="muted small">Found ${drugMatches.length}${drugMatches.length === 25 ? "+" : ""} medicines and ${encMatches.length} encyclopedia matches for <b>${q}</b>.</p>\n        ${drugMatches.length ? html`\n          <h2>Medicines (${drugMatches.length}${drugMatches.length === 25 ? "+" : ""})</h2>\n          <ul class="plain">${drugMatches.map((d) => html`<li><a href="${drugBase}${d.id}"><b>${d.name}</b></a>${d.year ? ` (${d.year})` : ""}</li>`)}</ul>\n        ` : ""}\n        ${[...grouped.entries()].map(([grp, list]) => html`\n          <h2>${grp} (${list.length})</h2>\n          <ul class="plain">${list.map((m) => html`<li>\n            <a href="${mode === "explore" ? m.href_explore : m.href_ref}"><b>${m.title}</b></a>\n            <br><span class="muted small">${m.summary}</span>\n          </li>`)}</ul>\n        `)}\n        ${!drugMatches.length && !encMatches.length ? html`<p>No matches found for "${q}". Try a broader term like <code>HPLC</code>, <code>Phase 2</code>, <code>bioreactor</code>, or <code>insulin</code>.</p>` : ""}\n      `}\n    `,\n    afterRender() {\n      const form = document.getElementById("gs-form");\n      if (form) {\n        form.addEventListener("submit", (ev) => {\n          ev.preventDefault();\n          const val = (document.getElementById("gs-input")?.value || "").trim();\n          location.hash = val ? `${baseRoute}?q=${encodeURIComponent(val)}` : baseRoute;\n        });\n      }\n    },\n  };\n}\n'
ORIGINS_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nexport async function originsGalleryPage(query) {\n  const doc = await getJSON("data/origins_gallery.json");\n  const all = doc.stories || [];\n  const cats = doc.categories || [];\n  const selectedCat = (query && query.get("cat")) || "";\n  const q = ((query && query.get("q")) || "").trim().toLowerCase();\n\n  const filtered = all.filter((s) => {\n    if (selectedCat && s.category !== selectedCat) return false;\n    if (q && !(`${s.medicine} ${s.category} ${s.simple} ${s.expert}`.toLowerCase().includes(q))) return false;\n    return true;\n  });\n\n  return {\n    title: "Discovery Origin Stories Gallery (75 Landmark Medicines)",\n    body: html`\n      <h1>How Landmark Medicines Were Discovered (${all.length} Stories)</h1>\n      <p class="lead">Every story below is verified against primary scientific literature (NIH PMC &amp; NobelPrize.org). Filter by how the medicine was discovered or jump to a random story.</p>\n      <p class="small">\n        <button id="origin-random-btn" type="button">Random Discovery Story</button> ·\n        <a href="#/explore/origins"${!selectedCat ? \' aria-current="page"\' : ""}>All (${all.length})</a>\n        ${cats.map((c) => html` · <a href="#/explore/origins?cat=${encodeURIComponent(c.name)}"${selectedCat === c.name ? \' aria-current="page"\' : ""}>${c.name} (${c.count})</a>`)}\n      </p>\n      <div class="cards-grid">\n        ${filtered.map((s) => html`<article class="x-panel" id="origin-${s.slug}">\n          <h2><a href="#/explore/medicine/${s.slug}/made">${s.medicine}</a></h2>\n          <p class="muted small">${s.category} · Checked ${s.checked}</p>\n          <p>${s.simple}</p>\n          <p class="muted small">Sources: ${(s.sources || []).map((src) => html`<a href="${src.url}" target="_blank" rel="noopener">${src.label}</a>`).join(" · ")}</p>\n        </article>`)}\n      </div>\n    `,\n    afterRender() {\n      const btn = document.getElementById("origin-random-btn");\n      if (btn && all.length) {\n        btn.addEventListener("click", () => {\n          const pick = all[Math.floor(Math.random() * all.length)];\n          location.hash = `#/explore/medicine/${pick.slug}/made`;\n        });\n      }\n    },\n  };\n}\n'


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
    for imp in [
        'import { globalSearchPage } from "./global_search.js";\n',
        'import { originsGalleryPage } from "./origins.js";\n',
    ]:
        if imp.split("from ")[1].strip() not in txt:
            txt = imp + txt
            changed = True
    if '"/ref/search"' not in txt:
        for anchor in ('if (path === "/ref/playbooks")', 'if (path === "/ref/partners")', 'if (path === "/ref/software")', 'if (path === "/ref/equipment")'):
            if anchor in txt:
                rep = (
                    'if (path === "/search" || path === "/ref/search") return globalSearchPage(query, "ref");\n'
                    '  if (path === "/explore/search") return globalSearchPage(query, "explore");\n'
                    '  if (path === "/explore/origins") return originsGalleryPage(query);\n'
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
    if "#/ref/search" not in txt:
        anchor = "const REF_NAV = ["
        if anchor in txt:
            txt = txt.replace(anchor, anchor + '\n  ["#/ref/search", "Global search"],', 1)
            changed = True
    if "#/explore/origins" not in txt:
        anchor = "const EXPLORE_NAV = ["
        if anchor in txt:
            txt = txt.replace(
                anchor,
                anchor
                + '\n  ["#/explore/search", "Search all"],'
                + '\n  ["#/explore/origins", "Origin stories (75)"],'
                + '\n  ["#/explore/playbooks", "5 medicine types"],'
                + '\n  ["#/explore/economics", "Funding & pricing"],'
                + '\n  ["#/explore/partners", "Who builds drugs"],',
                1,
            )
            changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_csv_hook(path: pathlib.Path, export_fn_name: str) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "./csv_export.js" in txt:
        return False
    header = 'import { downloadCsv } from "./csv_export.js";\n'
    helper = (
        f"\nexport function {export_fn_name}(rows = []) {{\n"
        f'  const cols = rows.length ? Object.keys(rows[0]).filter((k) => typeof rows[0][k] !== "object").map((k) => ({{ key: k, label: k }})) : [{{ key: "id", label: "id" }}];\n'
        f'  downloadCsv("{export_fn_name}.csv", cols, rows);\n'
        f"}}\n"
    )
    path.write_text(header + txt.rstrip() + "\n" + helper, encoding="utf-8")
    return True


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_global_search.py" in txt:
        return False
    hook = (
        "\n# v6.1a: Browsable 75-Origin-Stories Gallery & Unified Global Search Index\n"
        "python3 pipeline/build_origins_gallery.py pipeline/origin_stories.json site/data\n"
        "python3 pipeline/build_global_search.py site/data\n"
    )
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/search"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/search")\n'
        'def api_global_search(q: str = ""):\n'
        '    doc = _read_json(SITE_DIR / "data" / "global_search.json")\n'
        '    ql = q.strip().lower()\n'
        '    if not ql:\n'
        '        return doc\n'
        '    hits = [e for e in doc.get("entries", []) if ql in f"{e.get(\'title\',\'\')} {e.get(\'summary\',\'\')} {e.get(\'keywords\',\'\')}".lower()]\n'
        '    return {"query": q, "count": len(hits), "entries": hits[:60]}\n\n'
        '@app.get("/api/origins")\n'
        'def api_origins():\n'
        '    return _read_json(SITE_DIR / "data" / "origins_gallery.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_global_search_py": _write_if_changed(pipe_dir / "build_global_search.py", BUILD_GLOBAL_SEARCH_PY),
        "build_origins_gallery_py": _write_if_changed(pipe_dir / "build_origins_gallery.py", BUILD_ORIGINS_GALLERY_PY),
        "csv_export_js": _write_if_changed(js_dir / "csv_export.js", CSV_EXPORT_JS),
        "global_search_js": _write_if_changed(js_dir / "global_search.js", GLOBAL_SEARCH_JS),
        "origins_js": _write_if_changed(js_dir / "origins.js", ORIGINS_JS),
        "app_js_wired": _patch_app_js(js_dir / "app.js"),
        "layout_js_wired": _patch_layout_js(js_dir / "layout.js"),
        "vendors_csv_wired": _patch_csv_hook(js_dir / "vendors.js", "exportVendorsCsv"),
        "equipment_csv_wired": _patch_csv_hook(js_dir / "equipment.js", "exportEquipmentCsv"),
        "run_all_sh_hooked": _patch_run_all(pipe_dir / "run_all.sh"),
        "app_py_api_added": _patch_app_py(root / "app.py"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        (root / "site" / "data").mkdir(parents=True)

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/playbooks") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV = [\n];\nconst EXPLORE_NAV = [\n];\n', encoding="utf-8")
        (root / "site" / "js" / "vendors.js").write_text("export async function vendorsPage() {}\n", encoding="utf-8")
        (root / "site" / "js" / "equipment.js").write_text("export async function equipmentPage() {}\n", encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "origin_stories.json").write_text(json.dumps({
            "stories": [
                {"medicine": "ASPIRIN", "category": "Natural product", "simple": "Willow bark", "expert": "Salicylic acid", "sources": [{"label": "PMC", "url": "https://pmc.ncbi.nlm.nih.gov/"}], "checked": "2026-11-21"},
                {"medicine": "CIMETIDINE", "category": "Rational drug design", "simple": "H2 blocker", "expert": "Sir James Black", "sources": [{"label": "Nobel", "url": "https://www.nobelprize.org/"}], "checked": "2026-11-21"},
            ]
        }), encoding="utf-8")
        (root / "site" / "data" / "equipment.json").write_text(json.dumps([
            {"id": "eq-hplc-uplc", "name": "HPLC / UPLC", "department": "analytical", "plain_summary": "Separates drug molecules", "leading_oems": [{"name": "Waters"}], "technical_spec": {"primary_use": "Assay", "gmp_compliance": "21 CFR Part 11"}}
        ]), encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_global_search.py"), doraise=True)
        py_compile.compile(str(root / "pipeline" / "build_origins_gallery.py"), doraise=True)

        o_out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_origins_gallery.py"), str(root / "pipeline" / "origin_stories.json"), str(root / "site" / "data")],
            text=True,
        ))
        assert o_out["origins_gallery_stories"] == 2 and o_out["categories"] == 2, o_out

        gs_out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_global_search.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert gs_out["global_search_entries"] == 3, gs_out

        print("V61A_GLOBAL_SEARCH_ORIGINS_CSV_SELFTEST_PASSED", json.dumps({**o_out, **gs_out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1a Global Search, Origins Gallery & CSV Export patch.")
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
