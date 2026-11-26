#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch: Grouped Explore (Simple Mode) Navigation Module.

Why:
  Claude's 2026-11-26 08:20 ET update cleanly organized In-depth (`ref_nav.js`) into
  7 collapsible sections + a role shortlist. However, Simple mode (`EXPLORE_NAV`) still
  accumulates dozens of flat v6.1-v6.2 links as new modules are added, creating the same
  mobile link-wall clutter for students, parents, and teachers.

Fix:
  Stages a clean, zero-MutationObserver ES module `.github/site-fixes/js/explore_nav.js`
  plus companion stylesheet `.github/site-fixes/css/explore_nav.css` (mirroring Claude's
  `ref_nav.js` pattern) that groups Explore links into:
    - Core bar (always visible, 1 tap): Home, Medicines, Stories, How drugs are built, Quiz
    - 4 collapsible topic drawers (closed by default on phones):
        1. Discover & compare
        2. How medicines are made
        3. Safety & global health
        4. Classroom, careers & costs
    - Any unrecognized/future Explore link automatically lands under "More topics" so
      nothing is ever hidden or broken.

Usage:
  python3 2026-11-26_explore_nav_grouped_cleanup_patch.py --selftest
  python3 2026-11-26_explore_nav_grouped_cleanup_patch.py --apply /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile

EXPLORE_NAV_JS = """// Grouped, collapsible navigation for Simple / Explore mode (mirrors ref_nav.js)
// Wire into exploreShell() in site/js/layout.js via prepare_pages.py.
import { html } from "./ui.js";

export const EXPLORE_CORE_HREFS = new Set([
  "#/explore",
  "#/explore/medicines",
  "#/explore/origins",
  "#/explore/how-drugs-are-built",
  "#/explore/quiz",
]);

export const EXPLORE_SECTIONS = [
  {
    id: "discover",
    label: "Discover & compare",
    slugs: [
      "search", "history", "origins", "trace", "playbooks", "adme",
      "discovery-sbdd-protacs", "biologics", "vaccines", "radiopharma",
      "adcs-bispecifics-oligos", "rmat-hctp-cgt-cmc", "combo-products",
      "combo-devices", "diagnostics", "cdx",
    ],
  },
  {
    id: "made",
    label: "How medicines are made",
    slugs: [
      "how-drugs-are-built", "departments", "sterile", "continuous-pat-ai",
      "analytical-usp-q12", "excipients-dmfs-nano", "complex-quality",
      "packaging-el-dscsa", "supply-chain", "shortages", "shortages-resilience",
      "partners",
    ],
  },
  {
    id: "safety",
    label: "Safety & global health",
    slugs: [
      "trials", "safety", "pv-faers-sentinel", "inspections-483-recalls",
      "labeling-spl-rems", "pathways", "global-reg", "history-laws",
      "special-populations", "orphan", "rare-pediatric", "otc", "otc-compounding",
      "controlled-substances", "amr", "amr-antiinfectives", "rwe",
      "digital-health", "pfdd-coa-expanded-access", "oncology-oce",
      "nonclinical-nams", "babe-bcs-nti", "midd-pharmacometrics",
      "gcp-bimo-cdisc", "promotion-transparency",
    ],
  },
  {
    id: "classroom",
    label: "Classroom, careers & costs",
    slugs: [
      "teach", "worksheets", "glossary", "careers", "economics",
      "pricing-access", "ip", "bd-deals", "user-fees-prv",
    ],
  },
];

function slugFromHref(href) {
  const m = String(href || "").match(/^#\\/explore\\/([^/?#]+)/);
  return m ? m[1] : "";
}

export function renderGroupedExploreNav(items, current) {
  const list = Array.isArray(items) ? items : [];
  const core = [];
  const bySection = new Map(EXPLORE_SECTIONS.map((s) => [s.id, []]));
  const extra = [];

  for (const item of list) {
    if (EXPLORE_CORE_HREFS.has(item.href)) {
      core.push(item);
      continue;
    }
    const slug = slugFromHref(item.href);
    const sec = EXPLORE_SECTIONS.find((s) => s.slugs.includes(slug));
    if (sec) {
      bySection.get(sec.id).push(item);
    } else {
      extra.push(item);
    }
  }

  const isCurrent = (item) =>
    current && (item.href === current || slugFromHref(item.href) === current);

  const linkHtml = (item) =>
    html`<a class="x-nav-link" href="${item.href}" aria-current="${isCurrent(item) ? "page" : "false"}">${item.label}</a>`;

  const drawers = EXPLORE_SECTIONS.map((sec) => {
    const secItems = bySection.get(sec.id) || [];
    if (!secItems.length) return "";
    const openHere = secItems.some(isCurrent);
    return html`<details class="x-nav-group" ${openHere ? "open" : ""}>
      <summary>${sec.label} <span class="x-nav-count">(${secItems.length})</span></summary>
      <div class="x-nav-group-links">${secItems.map(linkHtml)}</div>
    </details>`;
  });

  if (extra.length) {
    const openExtra = extra.some(isCurrent);
    drawers.push(
      html`<details class="x-nav-group" ${openExtra ? "open" : ""}>
        <summary>More topics <span class="x-nav-count">(${extra.length})</span></summary>
        <div class="x-nav-group-links">${extra.map(linkHtml)}</div>
      </details>`
    );
  }

  return html`<nav class="x-grouped-nav" aria-label="Explore topics">
    <div class="x-nav-core">${core.map(linkHtml)}</div>
    <div class="x-nav-drawers">${drawers}</div>
  </nav>`;
}
"""

EXPLORE_NAV_CSS = """/* Grouped Explore / Simple mode navigation */
.x-grouped-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 8px 0 12px;
}

.x-nav-core {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.x-nav-core .x-nav-link {
  padding: 6px 12px;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.9rem;
  text-decoration: none;
  background: var(--paper, #ffffff);
  border: 1px solid rgba(22, 35, 59, 0.16);
}

.x-nav-drawers {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 6px;
}

.x-nav-group {
  border: 1px solid rgba(22, 35, 59, 0.14);
  border-radius: 10px;
  background: var(--paper, #ffffff);
  padding: 6px 10px;
}

.x-nav-group > summary {
  cursor: pointer;
  font-weight: 600;
  font-size: 0.88rem;
  list-style: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.x-nav-group > summary::-webkit-details-marker {
  display: none;
}

.x-nav-count {
  opacity: 0.65;
  font-weight: 500;
  font-size: 0.82rem;
}

.x-nav-group-links {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}

.x-nav-group-links .x-nav-link {
  padding: 4px 9px;
  border-radius: 8px;
  font-size: 0.84rem;
  text-decoration: none;
  background: rgba(22, 35, 59, 0.06);
}
"""


def apply_patch(root: pathlib.Path) -> dict:
    js_dir = root / ".github" / "site-fixes" / "js"
    css_dir = root / ".github" / "site-fixes" / "css"
    js_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)

    changed: list[str] = []
    js_path = js_dir / "explore_nav.js"
    if not js_path.is_file() or js_path.read_text(encoding="utf-8") != EXPLORE_NAV_JS:
        js_path.write_text(EXPLORE_NAV_JS, encoding="utf-8")
        changed.append(str(js_path.relative_to(root)))

    css_path = css_dir / "explore_nav.css"
    if not css_path.is_file() or css_path.read_text(encoding="utf-8") != EXPLORE_NAV_CSS:
        css_path.write_text(EXPLORE_NAV_CSS, encoding="utf-8")
        changed.append(str(css_path.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        js_txt = (root / ".github" / "site-fixes" / "js" / "explore_nav.js").read_text(encoding="utf-8")
        assert "renderGroupedExploreNav" in js_txt
        assert "MutationObserver" not in js_txt
        assert "var(--card" not in (root / ".github" / "site-fixes" / "css" / "explore_nav.css").read_text(encoding="utf-8")

        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("EXPLORE_NAV_GROUPED_CLEANUP_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage grouped Explore/Simple navigation module for site-fixes")
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
