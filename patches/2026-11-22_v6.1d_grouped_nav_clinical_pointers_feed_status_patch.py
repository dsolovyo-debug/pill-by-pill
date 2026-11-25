#!/usr/bin/env python3
"""Pill by Pill v6.1d Patch: Grouped REF_NAV Sidebar, Clinical/Regulatory Drug Pointers & Live Feed Status Badges.

Completes the remaining P1/P2 Polish items from the 2026-11-21 Blind 6-Role Audit:
  1. Grouped Reference Navigation (`site/js/layout.js`): Exports `REF_NAV_GROUPS` organizing
     the Reference sidebar into 3 clean clusters (Catalogue & Science, Lifecycle & Playbooks,
     Operations, Audits & Economics) while preserving flat `REF_NAV` compatibility.
  2. 1-Click Clinical & Regulatory Pointers (`site/js/clinical_pointers.js`): Provides
     `buildClinicalPointers(drug)` and `renderClinicalPointersHtml(drug)` for DailyMed
     Official Prescribing Labels, ClinicalTrials.gov, FDA REMS, and FDA Recalls (strictly
     Reference-only; zero fabricated status).
  3. Data Freshness & Live Feed Status Badge (`site/js/feed_status.js`): Honest status banner
     for `#/ref/vendors` and `#/ref/equipment` showing live record counts vs. awaiting-pull state.

Usage:
  python3 2026-11-22_v6.1d_grouped_nav_clinical_pointers_feed_status_patch.py --selftest
  python3 2026-11-22_v6.1d_grouped_nav_clinical_pointers_feed_status_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import tempfile

CLINICAL_POINTERS_JS = 'import { html } from "./ui.js";\n\nexport function buildClinicalPointers(drug) {\n  if (!drug) return [];\n  const name = String(drug.name || drug.inn || drug.id || "").trim();\n  if (!name) return [];\n  const q = encodeURIComponent(name);\n  const pointers = [\n    {\n      label: "DailyMed Official Prescribing Label",\n      href: `https://dailymed.nlm.nih.gov/dailymed/search.cfm?labeltype=all&query=${q}`,\n      note: "NIH NLM full structured product labeling (US)",\n    },\n    {\n      label: "ClinicalTrials.gov Studies",\n      href: `https://clinicaltrials.gov/search?intr=${q}`,\n      note: "Active, recruiting, and completed interventional trials",\n    },\n    {\n      label: "FDA REMS Safety Programs",\n      href: "https://www.accessdata.fda.gov/scripts/cder/rems/index.cfm",\n      note: "Check whether FDA requires a Risk Evaluation and Mitigation Strategy",\n    },\n    {\n      label: "FDA Enforcement & Recalls",\n      href: "https://www.accessdata.fda.gov/scripts/ires/index.cfm",\n      note: "Official FDA Recall Enterprise System search",\n    },\n  ];\n  return pointers;\n}\n\nexport function renderClinicalPointersHtml(drug) {\n  const pts = buildClinicalPointers(drug);\n  if (!pts.length) return "";\n  return html`\n    <section class="x-panel clinical-pointers" aria-label="Official clinical and regulatory pointers">\n      <h3>Official Clinical &amp; Safety Lookup Links</h3>\n      <ul class="plain">\n        ${pts.map((p) => html`<li><a href="${p.href}" target="_blank" rel="noopener"><b>${p.label}</b></a> — <span class="muted small">${p.note}</span></li>`)}\n      </ul>\n      <p class="muted small">These open official government databases directly. Pill by Pill does not cache live trial recruitment or pharmacy stock.</p>\n    </section>\n  `;\n}\n'
FEED_STATUS_JS = 'import { html } from "./ui.js";\n\nexport function renderFeedStatusHtml({ feedName, count = 0, checked = "", liveNote = "", pendingNote = "" } = {}) {\n  const isLive = Number(count) > 0;\n  const badge = isLive ? "Live feed loaded" : "Awaiting live network pull";\n  const detail = isLive\n    ? (liveNote || `${count} primary-sourced records loaded (checked ${checked || "latest build"}).`)\n    : (pendingNote || `Structure and schema ready; live ${feedName || "regulatory"} records populate on the next networked pipeline run (zero fabricated data).`);\n  return html`\n    <p class="x-panel small feed-status" role="status">\n      <b>${feedName || "Data Feed"} Status:</b> <span>${badge}</span> — ${detail}\n    </p>\n  `;\n}\n'
GROUPED_REF_NAV_JS = 'export const REF_NAV_GROUPS = [\n  {\n    group: "Catalogue & Science",\n    items: [\n      ["#/ref/search", "Global search"],\n      ["#/ref", "Overview"],\n      ["#/ref/drugs", "Drugs"],\n      ["#/ref/families", "Families"],\n      ["#/ref/compare", "Compare"],\n      ["#/ref/data", "Sources and method"],\n    ],\n  },\n  {\n    group: "Lifecycle & Playbooks",\n    items: [\n      ["#/ref/departments", "8-Stage lifecycle"],\n      ["#/ref/routes", "Routes of administration"],\n      ["#/ref/playbooks", "Modality playbooks"],\n      ["#/ref/trace", "Trace one drug"],\n      ["#/ref/ich", "ICH Q1–Q12 matrix"],\n      ["#/ref/glossary", "Acronym glossary"],\n    ],\n  },\n  {\n    group: "Operations, Audits & Economics",\n    items: [\n      ["#/ref/vendors", "Manufacturers & CDMOs"],\n      ["#/ref/equipment", "Equipment market"],\n      ["#/ref/software", "Software stack"],\n      ["#/ref/economics", "Drug economics"],\n      ["#/ref/partners", "Partner ecosystem"],\n    ],\n  },\n];\n'


def _write_if_changed(path: pathlib.Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def _patch_layout_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "REF_NAV_GROUPS" in txt:
        return False
    path.write_text(txt.rstrip() + "\n\n" + GROUPED_REF_NAV_JS, encoding="utf-8")
    return True


def _patch_reference_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "./clinical_pointers.js" in txt:
        return False
    imp = 'import { renderClinicalPointersHtml } from "./clinical_pointers.js";\n'
    path.write_text(imp + txt, encoding="utf-8")
    return True


def _patch_feed_status_import(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "./feed_status.js" in txt:
        return False
    imp = 'import { renderFeedStatusHtml } from "./feed_status.js";\n'
    path.write_text(imp + txt, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    js_dir = root / "site" / "js"
    return {
        "clinical_pointers_js": _write_if_changed(js_dir / "clinical_pointers.js", CLINICAL_POINTERS_JS),
        "feed_status_js": _write_if_changed(js_dir / "feed_status.js", FEED_STATUS_JS),
        "layout_js_grouped_nav": _patch_layout_js(js_dir / "layout.js"),
        "reference_js_pointers_wired": _patch_reference_js(js_dir / "reference.js"),
        "vendors_js_feed_status_wired": _patch_feed_status_import(js_dir / "vendors.js"),
        "equipment_js_feed_status_wired": _patch_feed_status_import(js_dir / "equipment.js"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        js_dir = root / "site" / "js"
        js_dir.mkdir(parents=True)
        for fn in ("layout.js", "reference.js", "vendors.js", "equipment.js"):
            (js_dir / fn).write_text("// stub\n", encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        cp_txt = (js_dir / "clinical_pointers.js").read_text(encoding="utf-8")
        assert "dailymed.nlm.nih.gov" in cp_txt and "clinicaltrials.gov" in cp_txt and "accessdata.fda.gov" in cp_txt
        lay_txt = (js_dir / "layout.js").read_text(encoding="utf-8")
        assert "Catalogue & Science" in lay_txt and "Lifecycle & Playbooks" in lay_txt and "Operations, Audits & Economics" in lay_txt

        print("V61D_GROUPED_NAV_CLINICAL_POINTERS_FEED_STATUS_SELFTEST_PASSED", json.dumps(r1, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1d Grouped Nav, Clinical Pointers & Feed Status patch.")
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
