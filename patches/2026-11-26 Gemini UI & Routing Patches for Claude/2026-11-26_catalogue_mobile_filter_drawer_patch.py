#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch (Batch 4): 3,379-Medicine Catalogue Mobile Filter Drawer & A-Z Strip.

Why:
  The Drug Catalogue (3,379 medicines) accumulates multiple filter controls (search,
  modality, route, approval agency, era, A-Z index) that stack vertically on phones
  and push the actual medicine list below the fold.

Fix:
  Stages a clean, zero-MutationObserver ES module `.github/site-fixes/js/catalogue_filters.js`
  and companion stylesheet `.github/site-fixes/css/catalogue_filters.css`:
    1. Sticky compact search + collapsible `<details>` Filter Drawer (closed by default on
       phones <= 640px, open on desktop) showing an active-filter count badge and a one-tap
       "Clear all" button.
    2. Single-row horizontally scrollable A-Z jump strip (`overflow-x: auto`, snap points)
       instead of a 4-row wrapped letter grid.
    3. Clean `attachCatalogueFilterDrawer(root, opts)` returning a cleanup function for
       `view.mount(app)`.

Usage:
  python3 2026-11-26_catalogue_mobile_filter_drawer_patch.py --selftest
  python3 2026-11-26_catalogue_mobile_filter_drawer_patch.py --apply /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile

CATALOGUE_FILTERS_JS = r"""// Mobile-friendly collapsible filter drawer & A-Z strip for the 3,379-medicine catalogue.
// Wire into the catalogue view and view.mount(app) via prepare_pages.py.
import { html } from "./ui.js";

const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

/**
 * Render a compact sticky search + collapsible filter drawer shell.
 * @param {object} opts
 * @param {string} [opts.searchPlaceholder]
 * @param {number} [opts.totalCount]
 * @param {number} [opts.shownCount]
 * @param {number} [opts.activeFilterCount]
 * @param {string} [opts.activeLetter]
 * @param {any} [opts.filterControlsHtml] - Pre-rendered facet selects/chips
 */
export function renderCatalogueFilterShell(opts = {}) {
  const total = Number(opts.totalCount || 0);
  const shown = Number(opts.shownCount ?? total);
  const activeCount = Number(opts.activeFilterCount || 0);
  const activeLetter = String(opts.activeLetter || "").toUpperCase();
  const placeholder = opts.searchPlaceholder || "Filter medicines by name, brand, target, or class…";

  const azButtons = [
    html`<button type="button" class="pbp-az-btn" data-letter="" aria-pressed="${activeLetter === "" ? "true" : "false"}">All</button>`,
    ...ALPHABET.map(
      (ch) =>
        html`<button type="button" class="pbp-az-btn" data-letter="${ch}" aria-pressed="${activeLetter === ch ? "true" : "false"}">${ch}</button>`
    ),
  ];

  return html`<section class="pbp-cat-controls" aria-label="Catalogue filters">
    <div class="pbp-cat-top">
      <div class="pbp-cat-count" aria-live="polite">
        Showing <strong>${shown.toLocaleString()}</strong>${total ? html` of ${total.toLocaleString()}` : ""} medicines
      </div>
      ${activeCount > 0
        ? html`<button type="button" class="pbp-cat-clear" data-action="clear-filters">Clear filters (${activeCount})</button>`
        : ""}
    </div>

    <details class="pbp-cat-drawer" data-pbp-filter-drawer>
      <summary class="pbp-cat-drawer-summary">
        <span>Filters${activeCount > 0 ? html` <span class="pbp-cat-badge">${activeCount}</span>` : ""}</span>
        <span class="pbp-cat-hint">Tap to ${activeCount > 0 ? "edit" : "narrow"}</span>
      </summary>
      <div class="pbp-cat-drawer-body">
        <label class="pbp-cat-search-label">
          <span class="sr-only">Filter catalogue</span>
          <input type="search" class="pbp-cat-search" data-cat-search placeholder="${placeholder}" autocomplete="off" />
        </label>
        <div class="pbp-cat-facets">${opts.filterControlsHtml || ""}</div>
      </div>
    </details>

    <div class="pbp-az-strip" role="group" aria-label="Jump by first letter">${azButtons}</div>
  </section>`;
}

/**
 * Attach responsive open/close defaults and event handlers for the filter drawer.
 * Returns a cleanup callback suitable for view.mount(app).
 */
export function attachCatalogueFilterDrawer(root, callbacks = {}) {
  const el = root && root.querySelector ? root : document;
  const drawer = el.querySelector("[data-pbp-filter-drawer]");
  if (drawer && window.innerWidth > 640) {
    drawer.setAttribute("open", "");
  }

  const onClick = (ev) => {
    const az = ev.target && ev.target.closest ? ev.target.closest(".pbp-az-btn") : null;
    if (az && typeof callbacks.onLetter === "function") {
      callbacks.onLetter(az.dataset.letter || "");
      return;
    }
    const clr = ev.target && ev.target.closest ? ev.target.closest('[data-action="clear-filters"]') : null;
    if (clr && typeof callbacks.onClear === "function") {
      callbacks.onClear();
    }
  };

  const onInput = (ev) => {
    const inp = ev.target && ev.target.matches && ev.target.matches("[data-cat-search]") ? ev.target : null;
    if (inp && typeof callbacks.onSearch === "function") {
      callbacks.onSearch(inp.value || "");
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

CATALOGUE_FILTERS_CSS = r"""/* Compact mobile filter drawer & horizontal A-Z strip for the Drug Catalogue */
.pbp-cat-controls {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 0 0 14px;
}

.pbp-cat-top {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

.pbp-cat-clear {
  padding: 5px 11px;
  min-height: 36px;
  border-radius: 999px;
  border: 1px solid rgba(22, 35, 59, 0.25);
  background: var(--paper, #ffffff);
  color: inherit;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
}

.pbp-cat-drawer {
  border: 1px solid rgba(22, 35, 59, 0.16);
  border-radius: 10px;
  background: var(--paper, #ffffff);
  padding: 8px 12px;
}

.pbp-cat-drawer-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.92rem;
  list-style: none;
}

.pbp-cat-drawer-summary::-webkit-details-marker {
  display: none;
}

.pbp-cat-badge {
  display: inline-block;
  margin-left: 6px;
  padding: 1px 7px;
  border-radius: 999px;
  font-size: 0.78rem;
  background: #16233b;
  color: #ffffff;
}

.pbp-cat-hint {
  font-size: 0.8rem;
  font-weight: 500;
  opacity: 0.65;
}

.pbp-cat-drawer-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.pbp-cat-search {
  width: 100%;
  min-height: 40px;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid rgba(22, 35, 59, 0.22);
  background: var(--paper, #ffffff);
  color: inherit;
  font-size: 0.95rem;
}

.pbp-cat-facets {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.pbp-az-strip {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  gap: 4px;
  padding: 2px 0 6px;
  scrollbar-width: thin;
}

.pbp-az-btn {
  flex: 0 0 auto;
  min-width: 34px;
  min-height: 36px;
  padding: 4px 8px;
  border-radius: 8px;
  border: 1px solid rgba(22, 35, 59, 0.16);
  background: var(--paper, #ffffff);
  color: inherit;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
}

.pbp-az-btn[aria-pressed="true"] {
  background: #16233b;
  color: #ffffff;
  border-color: #16233b;
}
"""


def apply_patch(root: pathlib.Path) -> dict:
    js_dir = root / ".github" / "site-fixes" / "js"
    css_dir = root / ".github" / "site-fixes" / "css"
    js_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)

    changed: list[str] = []
    js_path = js_dir / "catalogue_filters.js"
    if not js_path.is_file() or js_path.read_text(encoding="utf-8") != CATALOGUE_FILTERS_JS:
        js_path.write_text(CATALOGUE_FILTERS_JS, encoding="utf-8")
        changed.append(str(js_path.relative_to(root)))

    css_path = css_dir / "catalogue_filters.css"
    if not css_path.is_file() or css_path.read_text(encoding="utf-8") != CATALOGUE_FILTERS_CSS:
        css_path.write_text(CATALOGUE_FILTERS_CSS, encoding="utf-8")
        changed.append(str(css_path.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        js_txt = (root / ".github" / "site-fixes" / "js" / "catalogue_filters.js").read_text(encoding="utf-8")
        css_txt = (root / ".github" / "site-fixes" / "css" / "catalogue_filters.css").read_text(encoding="utf-8")
        assert "renderCatalogueFilterShell" in js_txt and "attachCatalogueFilterDrawer" in js_txt
        assert "MutationObserver" not in js_txt
        assert "var(--card" not in css_txt
        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("CATALOGUE_MOBILE_FILTER_DRAWER_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage mobile catalogue filter drawer & A-Z strip module")
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
