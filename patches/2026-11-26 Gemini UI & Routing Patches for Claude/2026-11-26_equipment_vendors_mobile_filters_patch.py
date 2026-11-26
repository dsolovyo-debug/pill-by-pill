#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch (Batch 5): Equipment Market & CDMOs Mobile Filters + Sticky Compare Tray.

Why:
  Both `#/ref/equipment` (18 hardware classes, OEM matrix, 5 Lab Kits) and `#/ref/vendors`
  (FEI sites, Parent Rollups, 3-site comparator) have multi-facet filters and view switchers
  that stack heavily on mobile, and selecting 2-3 sites to compare can lose the Compare
  button off-screen while scrolling.

Fix:
  Stages `.github/site-fixes/js/equipment_vendors_ui.js` and
  `.github/site-fixes/css/equipment_vendors_ui.css`:
    1. Segmented view-tab bar (`renderViewTabs`) with horizontal scroll on mobile.
    2. Collapsible `<details>` filter drawer (`renderMarketFilterDrawer`, closed on <= 640px,
       open on desktop) with active-filter count badge.
    3. Sticky bottom compare tray (`renderVendorCompareTray`) pinned above the safe area
       whenever 1-3 vendor FEIs are selected, with Clear and Compare (N/3) actions.
    4. Zero MutationObserver, zero `var(--card)`, safe tagged `html` templates.

Usage:
  python3 2026-11-26_equipment_vendors_mobile_filters_patch.py --selftest
  python3 2026-11-26_equipment_vendors_mobile_filters_patch.py --apply /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile

EQ_VENDORS_JS = r"""// Mobile-friendly view tabs, collapsible filter drawer & sticky compare tray for Equipment/Vendors.
// Wire into site/js/equipment.js and site/js/vendors.js via prepare_pages.py.
import { html } from "./ui.js";

/**
 * Render a horizontally scrollable segmented tab bar (e.g. All Classes / OEM Matrix / Lab Kits).
 * @param {Array<{href: string, label: string, active?: boolean}>} tabs
 */
export function renderViewTabs(tabs) {
  const list = Array.isArray(tabs) ? tabs : [];
  if (!list.length) return "";
  return html`<nav class="pbp-view-tabs" aria-label="View options">
    ${list.map(
      (t) =>
        html`<a class="pbp-view-tab" href="${t.href}" aria-current="${t.active ? "page" : "false"}">${t.label}</a>`
    )}
  </nav>`;
}

/**
 * Render a collapsible mobile filter drawer for Equipment Market or Manufacturers/CDMOs.
 * @param {{title?: string, activeCount?: number, bodyHtml: any}} opts
 */
export function renderMarketFilterDrawer(opts = {}) {
  const title = opts.title || "Filter list";
  const count = Number(opts.activeCount || 0);
  return html`<details class="pbp-mkt-drawer" data-pbp-mkt-drawer>
    <summary class="pbp-mkt-summary">
      <span>${title}${count > 0 ? html` <span class="pbp-mkt-badge">${count}</span>` : ""}</span>
      <span class="pbp-mkt-hint">Tap to ${count > 0 ? "adjust" : "filter"}</span>
    </summary>
    <div class="pbp-mkt-body">${opts.bodyHtml || ""}</div>
  </details>`;
}

/**
 * Render a sticky bottom selection tray for the 2-3 site CDMO/Manufacturer comparator.
 * @param {Array<{fei: string, name: string}>} selected
 */
export function renderVendorCompareTray(selected) {
  const items = (Array.isArray(selected) ? selected : []).slice(0, 3);
  if (!items.length) return "";
  const compareHref =
    items.length >= 2 ? `#/ref/vendors/compare/${items.map((x) => encodeURIComponent(x.fei)).join("/")}` : "";

  return html`<aside class="pbp-compare-tray" aria-label="Selected sites to compare">
    <div class="pbp-compare-chips">
      ${items.map(
        (s) =>
          html`<span class="pbp-compare-chip">
            ${s.name}
            <button type="button" class="pbp-chip-x" data-remove-fei="${s.fei}" aria-label="Remove ${s.name}">×</button>
          </span>`
      )}
    </div>
    <div class="pbp-compare-actions">
      <button type="button" class="pbp-tray-clear" data-tray-clear>Clear</button>
      ${compareHref
        ? html`<a class="pbp-tray-go" href="${compareHref}">Compare (${items.length}/3)</a>`
        : html`<span class="pbp-tray-need">Pick ${2 - items.length} more</span>`}
    </div>
  </aside>`;
}

/**
 * Open market filter drawers by default on desktop (> 640px) and wire tray events.
 */
export function attachMarketControls(root, callbacks = {}) {
  const el = root && root.querySelector ? root : document;
  if (window.innerWidth > 640) {
    el.querySelectorAll("[data-pbp-mkt-drawer]").forEach((d) => d.setAttribute("open", ""));
  }
  const onClick = (ev) => {
    const rm = ev.target && ev.target.closest ? ev.target.closest("[data-remove-fei]") : null;
    if (rm && typeof callbacks.onRemoveFei === "function") {
      callbacks.onRemoveFei(rm.dataset.removeFei);
      return;
    }
    const clr = ev.target && ev.target.closest ? ev.target.closest("[data-tray-clear]") : null;
    if (clr && typeof callbacks.onClear === "function") {
      callbacks.onClear();
    }
  };
  el.addEventListener("click", onClick);
  return () => el.removeEventListener("click", onClick);
}
"""

EQ_VENDORS_CSS = r"""/* Equipment Market & Manufacturers/CDMOs mobile tabs, filter drawer & sticky compare tray */
.pbp-view-tabs {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  gap: 6px;
  padding: 2px 0 10px;
  margin-bottom: 8px;
}

.pbp-view-tab {
  flex: 0 0 auto;
  min-height: 38px;
  display: inline-flex;
  align-items: center;
  padding: 6px 13px;
  border-radius: 999px;
  border: 1px solid rgba(22, 35, 59, 0.18);
  background: var(--paper, #ffffff);
  color: inherit;
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 600;
}

.pbp-view-tab[aria-current="page"] {
  background: #16233b;
  color: #ffffff;
  border-color: #16233b;
}

.pbp-mkt-drawer {
  border: 1px solid rgba(22, 35, 59, 0.16);
  border-radius: 10px;
  background: var(--paper, #ffffff);
  padding: 8px 12px;
  margin: 0 0 14px;
}

.pbp-mkt-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.92rem;
  list-style: none;
}

.pbp-mkt-summary::-webkit-details-marker {
  display: none;
}

.pbp-mkt-badge {
  display: inline-block;
  margin-left: 6px;
  padding: 1px 7px;
  border-radius: 999px;
  font-size: 0.78rem;
  background: #16233b;
  color: #ffffff;
}

.pbp-mkt-hint {
  font-size: 0.8rem;
  opacity: 0.65;
}

.pbp-mkt-body {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.pbp-compare-tray {
  position: sticky;
  bottom: max(10px, env(safe-area-inset-bottom, 10px));
  z-index: 20;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(22, 35, 59, 0.25);
  background: var(--paper, #ffffff);
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.16);
  margin-top: 14px;
}

.pbp-compare-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.pbp-compare-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 9px;
  border-radius: 999px;
  background: rgba(22, 35, 59, 0.08);
  font-size: 0.82rem;
  font-weight: 600;
}

.pbp-chip-x {
  border: 0;
  background: transparent;
  color: inherit;
  font-size: 1rem;
  line-height: 1;
  cursor: pointer;
  padding: 0 2px;
}

.pbp-compare-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pbp-tray-clear {
  min-height: 36px;
  padding: 5px 10px;
  border-radius: 8px;
  border: 1px solid rgba(22, 35, 59, 0.22);
  background: var(--paper, #ffffff);
  color: inherit;
  font-size: 0.84rem;
  cursor: pointer;
}

.pbp-tray-go {
  min-height: 36px;
  display: inline-flex;
  align-items: center;
  padding: 5px 13px;
  border-radius: 8px;
  background: #cc2f5a;
  color: #ffffff !important;
  text-decoration: none;
  font-size: 0.86rem;
  font-weight: 600;
}

.pbp-tray-need {
  font-size: 0.82rem;
  opacity: 0.7;
}
"""


def apply_patch(root: pathlib.Path) -> dict:
    js_dir = root / ".github" / "site-fixes" / "js"
    css_dir = root / ".github" / "site-fixes" / "css"
    js_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)

    changed: list[str] = []
    js_path = js_dir / "equipment_vendors_ui.js"
    if not js_path.is_file() or js_path.read_text(encoding="utf-8") != EQ_VENDORS_JS:
        js_path.write_text(EQ_VENDORS_JS, encoding="utf-8")
        changed.append(str(js_path.relative_to(root)))

    css_path = css_dir / "equipment_vendors_ui.css"
    if not css_path.is_file() or css_path.read_text(encoding="utf-8") != EQ_VENDORS_CSS:
        css_path.write_text(EQ_VENDORS_CSS, encoding="utf-8")
        changed.append(str(css_path.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        js_txt = (root / ".github" / "site-fixes" / "js" / "equipment_vendors_ui.js").read_text(encoding="utf-8")
        css_txt = (root / ".github" / "site-fixes" / "css" / "equipment_vendors_ui.css").read_text(encoding="utf-8")
        assert "renderVendorCompareTray" in js_txt and "attachMarketControls" in js_txt
        assert "MutationObserver" not in js_txt
        assert "var(--card" not in css_txt
        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("EQUIPMENT_VENDORS_MOBILE_FILTERS_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage Equipment & Vendors mobile filter and compare tray module")
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
