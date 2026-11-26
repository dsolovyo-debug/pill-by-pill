#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch: Grouped Explore (Simple) Navigation Module (`explore_nav.js`)
matching Claude's clean `ref_nav.js` architecture (zero MutationObserver, zero inline script dumps).

Why:
  Claude cleaned up In-depth navigation via `.github/site-fixes/js/ref_nav.js` (7 collapsible
  sections + role shortlist). Simple/Explore mode (`EXPLORE_NAV`) has also accumulated 25+
  flat links from v6.0-v6.2 patches. This module groups Explore links into 5 student-friendly
  collapsible `<details>` sections (closed by default on phones, active section open on desktop)
  and keeps student pages 100% free of commercial links.

Usage:
  python3 2026-11-26_explore_nav_grouping_and_mobile_polish_patch.py --selftest
  python3 2026-11-26_explore_nav_grouping_and_mobile_polish_patch.py --apply /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile

EXPLORE_NAV_JS = """// Grouped Simple/Explore navigation helper (parallel to ref_nav.js; zero MutationObserver)
import { html } from "./ui.js";

export const EXPLORE_SECTIONS = [
  {
    id: "start",
    title: "Start & Medicines",
    routes: [
      "#/explore",
      "#/explore/search",
      "#/explore/medicines",
      "#/explore/origins",
      "#/explore/trace",
    ],
  },
  {
    id: "how-made",
    title: "How Medicines Are Built",
    routes: [
      "#/explore/how-drugs-are-built",
      "#/explore/playbooks",
      "#/explore/adme",
      "#/explore/biologics",
      "#/explore/vaccines",
      "#/explore/combo-products",
      "#/explore/combo-devices",
      "#/explore/radiopharma",
      "#/explore/discovery-sbdd-protacs",
    ],
  },
  {
    id: "safety-trials",
    title: "Trials, Safety & Quality",
    routes: [
      "#/explore/trials",
      "#/explore/safety",
      "#/explore/pv-faers-sentinel",
      "#/explore/sterile",
      "#/explore/supply-chain",
      "#/explore/packaging-el-dscsa",
      "#/explore/shortages",
      "#/explore/shortages-resilience",
      "#/explore/inspections-483-recalls",
      "#/explore/labeling-spl-rems",
      "#/explore/nonclinical-nams",
      "#/explore/babe-bcs-nti",
      "#/explore/analytical-usp-q12",
      "#/explore/continuous-pat-ai",
    ],
  },
  {
    id: "policy-world",
    title: "History, Access & Careers",
    routes: [
      "#/explore/history",
      "#/explore/history-laws",
      "#/explore/pathways",
      "#/explore/global-reg",
      "#/explore/economics",
      "#/explore/pricing-access",
      "#/explore/partners",
      "#/explore/careers",
      "#/explore/orphan",
      "#/explore/rare-pediatric",
      "#/explore/special-populations",
      "#/explore/otc-compounding",
      "#/explore/user-fees-prv",
    ],
  },
  {
    id: "learn",
    title: "Quiz, Glossary & Teachers",
    routes: [
      "#/explore/quiz",
      "#/explore/glossary",
      "#/explore/worksheets",
      "#/explore/teach",
    ],
  },
];

export function renderExploreNav(navItems, currentHref = "") {
  const isPhone = typeof window !== "undefined" && window.innerWidth < 768;
  const byHref = new Map((navItems || []).map(([href, label]) => [href, label]));
  const placed = new Set();

  const sections = EXPLORE_SECTIONS.map((sec) => {
    const items = [];
    for (const href of sec.routes) {
      if (byHref.has(href)) {
        items.push([href, byHref.get(href)]);
        placed.add(href);
      }
    }
    return { ...sec, items };
  }).filter((sec) => sec.items.length > 0);

  const leftovers = (navItems || []).filter(([href]) => !placed.has(href));
  if (leftovers.length) {
    sections.push({ id: "more", title: "More topics", items: leftovers });
  }

  return html`<nav class="x-nav-grouped" aria-label="Explore sections">
    ${sections.map((sec) => {
      const hasCurrent = sec.items.some(([href]) => href === currentHref);
      const openAttr = !isPhone && (hasCurrent || sec.id === "start");
      return html`<details class="x-nav-group" ${openAttr ? html`open` : ""}>
        <summary>${sec.title} <span class="x-nav-count">(${sec.items.length})</span></summary>
        <div class="x-nav-links">
          ${sec.items.map(([href, label]) =>
            html`<a href="${href}" aria-current="${href === currentHref ? "page" : "false"}">${label}</a>`
          )}
        </div>
      </details>`;
    })}
  </nav>`;
}
"""

EXPLORE_NAV_CSS = """
/* Grouped Explore navigation (mobile-first collapsible sections) */
.x-nav-grouped { display: flex; flex-direction: column; gap: 6px; margin: 10px 0 16px; }
.x-nav-group { border: 1px solid var(--line, #e2d9ce); border-radius: 10px; background: var(--paper, #fff); padding: 6px 10px; }
.x-nav-group > summary { cursor: pointer; font-weight: 700; font-size: 0.92rem; list-style: none; display: flex; justify-content: space-between; align-items: center; }
.x-nav-group > summary::-webkit-details-marker { display: none; }
.x-nav-count { font-weight: 400; opacity: 0.7; font-size: 0.84rem; }
.x-nav-links { display: flex; flex-wrap: wrap; gap: 6px; padding-top: 8px; }
.x-nav-links a { padding: 5px 10px; border-radius: 999px; font-size: 0.86rem; text-decoration: none; border: 1px solid var(--line, #e2d9ce); }
.x-nav-links a[aria-current="page"] { font-weight: 700; border-color: currentColor; }
"""


def apply_patch(root: pathlib.Path) -> dict:
    changed = []
    fixes_js = root / ".github" / "site-fixes" / "js"
    js_dir = fixes_js if fixes_js.is_dir() else (root / "site" / "js")
    js_dir.mkdir(parents=True, exist_ok=True)
    target_js = js_dir / "explore_nav.js"
    if not target_js.is_file() or target_js.read_text(encoding="utf-8") != EXPLORE_NAV_JS:
        target_js.write_text(EXPLORE_NAV_JS, encoding="utf-8")
        changed.append(str(target_js.relative_to(root)))

    css_file = root / "site" / "css" / "explore.css"
    if css_file.is_file():
        raw_css = css_file.read_text(encoding="utf-8", errors="ignore")
        if ".x-nav-grouped" not in raw_css:
            css_file.write_text(raw_css.rstrip() + "\n" + EXPLORE_NAV_CSS, encoding="utf-8")
            changed.append(str(css_file.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / ".github" / "site-fixes" / "js").mkdir(parents=True)
        (root / "site" / "css").mkdir(parents=True)
        (root / "site" / "css" / "explore.css").write_text("body { margin: 0; }\n", encoding="utf-8")

        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        assert (root / ".github" / "site-fixes" / "js" / "explore_nav.js").is_file()
        assert ".x-nav-grouped" in (root / "site" / "css" / "explore.css").read_text(encoding="utf-8")

        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
    print("EXPLORE_NAV_GROUPING_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Add grouped Explore navigation helper and mobile CSS")
    ap.add_argument("--apply", type=pathlib.Path, help="Path to repo root")
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
