#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch (Batch 6): Medicine Families & WHO ATC Class Tree Mobile Accordions.

Why:
  `#/ref/families` (297 drug families, 1,105 medicines) and `#/ref/classes` (14 WHO ATC
  Level-1 organ systems + Level-2 therapeutic subgroups) render long nested lists that
  require heavy scrolling on phones when every group is expanded at once.

Fix:
  Stages `.github/site-fixes/js/families_atc_ui.js` and
  `.github/site-fixes/css/families_atc_ui.css`:
    1. Compact sticky search + Expand all / Collapse all toolbar (`renderTreeToolbar`).
    2. Native `<details>` accordion cards (`renderAtcOrganAccordion`, `renderFamilyAccordion`)
       with drug-count & WHO EML badges, closed by default on phones so all 14 ATC organ
       systems fit on ~1.5 screens.
    3. Clean `attachTreeAccordionControls(root, callbacks)` returning a cleanup hook for
       `view.mount(app)`.
    4. Zero MutationObserver, zero `var(--card)`, safe tagged `html` templates.

Usage:
  python3 2026-11-26_families_and_atc_tree_mobile_accordions_patch.py --selftest
  python3 2026-11-26_families_and_atc_tree_mobile_accordions_patch.py --apply /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile

FAMILIES_ATC_JS = r"""// Collapsible mobile accordions & instant filter bar for Medicine Families & WHO ATC Class Tree.
// Wire into site/js/families.js and site/js/atc_classes.js via prepare_pages.py.
import { html } from "./ui.js";

/**
 * Render a compact instant-filter input + Expand/Collapse all toolbar.
 * @param {{placeholder?: string, countLabel?: string}} opts
 */
export function renderTreeToolbar(opts = {}) {
  const placeholder = opts.placeholder || "Filter by class, stem, target, or medicine…";
  return html`<div class="pbp-tree-toolbar">
    <label class="pbp-tree-search-wrap">
      <span class="sr-only">Filter list</span>
      <input type="search" class="pbp-tree-search" data-tree-filter placeholder="${placeholder}" autocomplete="off" />
    </label>
    <div class="pbp-tree-actions">
      ${opts.countLabel ? html`<span class="pbp-tree-count">${opts.countLabel}</span>` : ""}
      <button type="button" class="pbp-tree-btn" data-tree-action="expand">Expand all</button>
      <button type="button" class="pbp-tree-btn" data-tree-action="collapse">Collapse all</button>
    </div>
  </div>`;
}

/**
 * Render a single collapsible WHO ATC Level-1 organ system accordion.
 * @param {{code: string, name: string, drugCount: number, emlCount?: number, bodyHtml: any, open?: boolean}} group
 */
export function renderAtcOrganAccordion(group) {
  return html`<details class="pbp-tree-acc" data-pbp-tree-acc ${group.open ? "open" : ""}>
    <summary class="pbp-tree-summary">
      <span class="pbp-tree-title">
        <span class="pbp-atc-code">${group.code}</span>
        <span>${group.name}</span>
      </span>
      <span class="pbp-tree-badges">
        <span class="pbp-tree-badge">${group.drugCount}</span>
        ${group.emlCount ? html`<span class="pbp-tree-badge pbp-eml-badge" title="WHO Essential Medicines">★ ${group.emlCount}</span>` : ""}
      </span>
    </summary>
    <div class="pbp-tree-body">${group.bodyHtml}</div>
  </details>`;
}

/**
 * Render a single collapsible Medicine Family accordion card.
 * @param {{stem: string, target: string, memberCount: number, pioneer?: string, bodyHtml: any, open?: boolean}} fam
 */
export function renderFamilyAccordion(fam) {
  return html`<details class="pbp-tree-acc" data-pbp-tree-acc ${fam.open ? "open" : ""}>
    <summary class="pbp-tree-summary">
      <span class="pbp-tree-title">
        <strong>${fam.stem}</strong>
        <span class="pbp-tree-sub">${fam.target}</span>
      </span>
      <span class="pbp-tree-badges">
        <span class="pbp-tree-badge">${fam.memberCount} drugs</span>
      </span>
    </summary>
    <div class="pbp-tree-body">${fam.bodyHtml}</div>
  </details>`;
}

/**
 * Wire filter input and Expand/Collapse all buttons. Returns cleanup function for view.mount(app).
 */
export function attachTreeAccordionControls(root, callbacks = {}) {
  const el = root && root.querySelector ? root : document;

  const onClick = (ev) => {
    const btn = ev.target && ev.target.closest ? ev.target.closest("[data-tree-action]") : null;
    if (!btn) return;
    const expand = btn.dataset.treeAction === "expand";
    el.querySelectorAll("details[data-pbp-tree-acc]").forEach((d) => {
      if (expand) d.setAttribute("open", "");
      else d.removeAttribute("open");
    });
  };

  const onInput = (ev) => {
    const inp = ev.target && ev.target.matches && ev.target.matches("[data-tree-filter]") ? ev.target : null;
    if (inp && typeof callbacks.onFilter === "function") {
      callbacks.onFilter(inp.value || "");
    }
  };

  el.addEventListener("click", onClick);
  el.addEventListener("input", onInput);
  return () => {
    el.removeEventListener("click", onClick);
    el.removeEventListener("input", onInput);
  };
}
"""

FAMILIES_ATC_CSS = r"""/* Medicine Families & WHO ATC Class Tree mobile-first accordions */
.pbp-tree-toolbar {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 0 0 14px;
}

.pbp-tree-search {
  width: 100%;
  min-height: 40px;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid rgba(22, 35, 59, 0.22);
  background: var(--paper, #ffffff);
  color: inherit;
  font-size: 0.94rem;
}

.pbp-tree-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
}

.pbp-tree-count {
  font-size: 0.84rem;
  opacity: 0.72;
  margin-right: auto;
}

.pbp-tree-btn {
  min-height: 36px;
  padding: 5px 11px;
  border-radius: 8px;
  border: 1px solid rgba(22, 35, 59, 0.2);
  background: var(--paper, #ffffff);
  color: inherit;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
}

.pbp-tree-acc {
  border: 1px solid rgba(22, 35, 59, 0.14);
  border-radius: 10px;
  background: var(--paper, #ffffff);
  margin-bottom: 8px;
  overflow: hidden;
}

.pbp-tree-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  cursor: pointer;
  list-style: none;
}

.pbp-tree-summary::-webkit-details-marker {
  display: none;
}

.pbp-tree-title {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  font-size: 0.94rem;
  font-weight: 600;
}

.pbp-tree-sub {
  font-weight: 400;
  font-size: 0.84rem;
  opacity: 0.76;
}

.pbp-atc-code {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 26px;
  height: 26px;
  border-radius: 6px;
  background: #16233b;
  color: #ffffff;
  font-size: 0.82rem;
  font-weight: 700;
}

.pbp-tree-badges {
  display: inline-flex;
  flex-shrink: 0;
  gap: 5px;
}

.pbp-tree-badge {
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 600;
  background: rgba(22, 35, 59, 0.08);
}

.pbp-eml-badge {
  background: rgba(204, 47, 90, 0.12);
  color: #cc2f5a;
}

.pbp-tree-body {
  padding: 8px 12px 12px;
  border-top: 1px solid rgba(22, 35, 59, 0.08);
}
"""


def apply_patch(root: pathlib.Path) -> dict:
    js_dir = root / ".github" / "site-fixes" / "js"
    css_dir = root / ".github" / "site-fixes" / "css"
    js_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)

    changed: list[str] = []
    js_path = js_dir / "families_atc_ui.js"
    if not js_path.is_file() or js_path.read_text(encoding="utf-8") != FAMILIES_ATC_JS:
        js_path.write_text(FAMILIES_ATC_JS, encoding="utf-8")
        changed.append(str(js_path.relative_to(root)))

    css_path = css_dir / "families_atc_ui.css"
    if not css_path.is_file() or css_path.read_text(encoding="utf-8") != FAMILIES_ATC_CSS:
        css_path.write_text(FAMILIES_ATC_CSS, encoding="utf-8")
        changed.append(str(css_path.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        js_txt = (root / ".github" / "site-fixes" / "js" / "families_atc_ui.js").read_text(encoding="utf-8")
        css_txt = (root / ".github" / "site-fixes" / "css" / "families_atc_ui.css").read_text(encoding="utf-8")
        assert "renderAtcOrganAccordion" in js_txt and "renderFamilyAccordion" in js_txt
        assert "MutationObserver" not in js_txt
        assert "var(--card" not in css_txt
        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("FAMILIES_AND_ATC_TREE_ACCORDIONS_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage Medicine Families & WHO ATC Class Tree mobile accordions")
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
