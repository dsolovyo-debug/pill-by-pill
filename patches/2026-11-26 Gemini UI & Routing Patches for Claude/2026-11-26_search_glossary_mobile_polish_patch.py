#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch (Batch 5): Global Search Category Tabs & Acronym Glossary Quick Bar.

Why:
  Global Search now spans 3,379 medicines plus 50+ encyclopedia modules, equipment classes,
  and 60 glossary terms. Returning all hits in one flat scroll makes mobile scanning slow,
  and the 60-term Acronym Glossary benefits from a single-row A-Z / domain chip bar.

Fix:
  Stages `.github/site-fixes/js/search_glossary_ui.js` and
  `.github/site-fixes/css/search_glossary_ui.css`:
    1. Category result tabs (`renderSearchCategoryTabs`) with live hit counts (All / Medicines /
       Encyclopedia / Equipment & CDMOs / Glossary) that scroll cleanly in one row on phones.
    2. Compact Glossary filter bar (`renderGlossaryQuickBar`) with domain chips and live
       instant filter input.
    3. Zero MutationObserver, zero `var(--card)`, safe tagged `html` templates.

Usage:
  python3 2026-11-26_search_glossary_mobile_polish_patch.py --selftest
  python3 2026-11-26_search_glossary_mobile_polish_patch.py --apply /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile

SEARCH_GLOSSARY_JS = r"""// Grouped category tabs for Global Search & compact filter strip for the 60-term Glossary.
// Wire into global_search.js and glossary view via prepare_pages.py.
import { html } from "./ui.js";

/**
 * Render horizontally scrollable category tabs with hit counts for Global Search.
 * @param {Array<{id: string, label: string, count: number}>} buckets
 * @param {string} activeId
 */
export function renderSearchCategoryTabs(buckets, activeId = "all") {
  const list = (Array.isArray(buckets) ? buckets : []).filter((b) => b && (b.id === "all" || b.count > 0));
  if (!list.length) return "";
  return html`<div class="pbp-search-tabs" role="tablist" aria-label="Search result categories">
    ${list.map(
      (b) => html`<button
        type="button"
        role="tab"
        class="pbp-search-tab"
        data-search-bucket="${b.id}"
        aria-selected="${b.id === activeId ? "true" : "false"}"
      >
        ${b.label} <span class="pbp-tab-count">${b.count}</span>
      </button>`
    )}
  </div>`;
}

/**
 * Render a compact instant-filter input + domain chip strip for the Acronym Glossary.
 * @param {Array<string>} categories
 * @param {string} activeCategory
 */
export function renderGlossaryQuickBar(categories, activeCategory = "All") {
  const cats = ["All", ...(Array.isArray(categories) ? categories.filter((c) => c && c !== "All") : [])];
  return html`<div class="pbp-gloss-bar">
    <label class="pbp-gloss-label">
      <span class="sr-only">Filter glossary terms</span>
      <input type="search" class="pbp-gloss-input" data-gloss-filter placeholder="Filter acronyms (e.g. IND, cGMP, REMS, DSCSA)…" autocomplete="off" />
    </label>
    <div class="pbp-gloss-chips" role="group" aria-label="Glossary categories">
      ${cats.map(
        (c) => html`<button
          type="button"
          class="pbp-gloss-chip"
          data-gloss-cat="${c}"
          aria-pressed="${c === activeCategory ? "true" : "false"}"
        >${c}</button>`
      )}
    </div>
  </div>`;
}

/**
 * Attach tab/filter handlers for Global Search or Glossary. Returns cleanup callback.
 */
export function attachSearchGlossaryControls(root, callbacks = {}) {
  const el = root && root.querySelector ? root : document;
  const onClick = (ev) => {
    const tab = ev.target && ev.target.closest ? ev.target.closest("[data-search-bucket]") : null;
    if (tab && typeof callbacks.onBucket === "function") {
      callbacks.onBucket(tab.dataset.searchBucket);
      return;
    }
    const chip = ev.target && ev.target.closest ? ev.target.closest("[data-gloss-cat]") : null;
    if (chip && typeof callbacks.onGlossaryCategory === "function") {
      callbacks.onGlossaryCategory(chip.dataset.glossCat);
    }
  };
  const onInput = (ev) => {
    const inp = ev.target && ev.target.matches && ev.target.matches("[data-gloss-filter]") ? ev.target : null;
    if (inp && typeof callbacks.onGlossaryQuery === "function") {
      callbacks.onGlossaryQuery(inp.value || "");
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

SEARCH_GLOSSARY_CSS = r"""/* Global Search category tabs & Acronym Glossary quick-filter bar */
.pbp-search-tabs,
.pbp-gloss-chips {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  gap: 6px;
  padding: 2px 0 8px;
}

.pbp-search-tab,
.pbp-gloss-chip {
  flex: 0 0 auto;
  min-height: 36px;
  padding: 5px 12px;
  border-radius: 999px;
  border: 1px solid rgba(22, 35, 59, 0.18);
  background: var(--paper, #ffffff);
  color: inherit;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
}

.pbp-search-tab[aria-selected="true"],
.pbp-gloss-chip[aria-pressed="true"] {
  background: #16233b;
  color: #ffffff;
  border-color: #16233b;
}

.pbp-tab-count {
  opacity: 0.72;
  font-weight: 500;
  margin-left: 3px;
}

.pbp-gloss-bar {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 0 0 14px;
}

.pbp-gloss-input {
  width: 100%;
  min-height: 40px;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid rgba(22, 35, 59, 0.22);
  background: var(--paper, #ffffff);
  color: inherit;
  font-size: 0.94rem;
}
"""


def apply_patch(root: pathlib.Path) -> dict:
    js_dir = root / ".github" / "site-fixes" / "js"
    css_dir = root / ".github" / "site-fixes" / "css"
    js_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)

    changed: list[str] = []
    js_path = js_dir / "search_glossary_ui.js"
    if not js_path.is_file() or js_path.read_text(encoding="utf-8") != SEARCH_GLOSSARY_JS:
        js_path.write_text(SEARCH_GLOSSARY_JS, encoding="utf-8")
        changed.append(str(js_path.relative_to(root)))

    css_path = css_dir / "search_glossary_ui.css"
    if not css_path.is_file() or css_path.read_text(encoding="utf-8") != SEARCH_GLOSSARY_CSS:
        css_path.write_text(SEARCH_GLOSSARY_CSS, encoding="utf-8")
        changed.append(str(css_path.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        js_txt = (root / ".github" / "site-fixes" / "js" / "search_glossary_ui.js").read_text(encoding="utf-8")
        css_txt = (root / ".github" / "site-fixes" / "css" / "search_glossary_ui.css").read_text(encoding="utf-8")
        assert "renderSearchCategoryTabs" in js_txt and "renderGlossaryQuickBar" in js_txt
        assert "MutationObserver" not in js_txt
        assert "var(--card" not in css_txt
        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("SEARCH_GLOSSARY_MOBILE_POLISH_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage Global Search category tabs & Glossary quick-filter module")
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
