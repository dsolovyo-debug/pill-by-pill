#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch (Batch 6): 100-Origin-Stories Gallery Filter Chips & Compact Cards.

Why:
  The 100-medicine Origin Stories Gallery (`#/explore/origins`) has multiple discovery
  categories (Accidental, Natural Product, Rational Design, Repurposed, Biologic, etc.)
  and rich multi-sentence narratives. On mobile, long unwrapped category buttons and full
  expanded paragraphs make browsing all 100 stories tiring.

Fix:
  Stages `.github/site-fixes/js/origins_gallery_ui.js` and
  `.github/site-fixes/css/origins_gallery_ui.css`:
    1. Single-row horizontally scrollable category filter chip strip + prominent
       "Random discovery story" button (`renderOriginsFilterBar`).
    2. Compact story cards (`renderOriginStoryCard`) showing drug name, category pill,
       and a 3-line CSS clamp preview with a native `<details>` "Read full story & sources"
       expander so mobile visitors can scan dozens of stories effortlessly.
    3. Clean `attachOriginsControls(root, callbacks)` returning a cleanup callback for
       `view.mount(app)`.
    4. Zero MutationObserver, zero `var(--card)`, safe tagged `html` templates.

Usage:
  python3 2026-11-26_origins_gallery_mobile_cards_patch.py --selftest
  python3 2026-11-26_origins_gallery_mobile_cards_patch.py --apply /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile

ORIGINS_GALLERY_JS = r"""// Horizontally scrollable category chips & compact expandable cards for the 100-Origin-Stories Gallery.
// Wire into site/js/origins.js and view.mount(app) via prepare_pages.py.
import { html } from "./ui.js";

/**
 * Render search input, Random Story action, and single-row category filter chips.
 * @param {Array<{label: string, count?: number}>} categories
 * @param {string} activeCategory
 */
export function renderOriginsFilterBar(categories, activeCategory = "All") {
  const list = [{ label: "All" }, ...(Array.isArray(categories) ? categories.filter((c) => c && c.label !== "All") : [])];

  return html`<section class="pbp-orig-bar" aria-label="Filter origin stories">
    <div class="pbp-orig-top">
      <label class="pbp-orig-search-wrap">
        <span class="sr-only">Search origin stories</span>
        <input type="search" class="pbp-orig-search" data-orig-search placeholder="Search 100 discovery stories (e.g. penicillin, venom, soil)…" autocomplete="off" />
      </label>
      <button type="button" class="pbp-orig-random" data-orig-random>Random story</button>
    </div>
    <div class="pbp-orig-chips" role="group" aria-label="Discovery categories">
      ${list.map(
        (c) => html`<button
          type="button"
          class="pbp-orig-chip"
          data-orig-cat="${c.label}"
          aria-pressed="${c.label === activeCategory ? "true" : "false"}"
        >
          ${c.label}${c.count !== undefined ? html` <span class="pbp-orig-cnt">${c.count}</span>` : ""}
        </button>`
      )}
    </div>
  </section>`;
}

/**
 * Render a compact scannable origin-story card with expandable full narrative & sources.
 * @param {{name: string, slug: string, category: string, preview: string, fullHtml?: any, href?: string}} story
 */
export function renderOriginStoryCard(story) {
  const href = story.href || `#/explore/medicine/${encodeURIComponent(story.slug || "")}/made`;
  return html`<article class="pbp-orig-card">
    <div class="pbp-orig-head">
      <h3 class="pbp-orig-title"><a href="${href}">${story.name}</a></h3>
      ${story.category ? html`<span class="pbp-orig-cat-tag">${story.category}</span>` : ""}
    </div>
    <p class="pbp-orig-preview">${story.preview}</p>
    ${story.fullHtml
      ? html`<details class="pbp-orig-more">
          <summary>Read full story &amp; sources</summary>
          <div class="pbp-orig-full">${story.fullHtml}</div>
        </details>`
      : ""}
  </article>`;
}

/**
 * Wire Origins Gallery search, category chips, and Random Story button. Returns cleanup callback.
 */
export function attachOriginsControls(root, callbacks = {}) {
  const el = root && root.querySelector ? root : document;

  const onClick = (ev) => {
    const chip = ev.target && ev.target.closest ? ev.target.closest("[data-orig-cat]") : null;
    if (chip && typeof callbacks.onCategory === "function") {
      callbacks.onCategory(chip.dataset.origCat);
      return;
    }
    const rnd = ev.target && ev.target.closest ? ev.target.closest("[data-orig-random]") : null;
    if (rnd && typeof callbacks.onRandom === "function") {
      callbacks.onRandom();
    }
  };

  const onInput = (ev) => {
    const inp = ev.target && ev.target.matches && ev.target.matches("[data-orig-search]") ? ev.target : null;
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

ORIGINS_GALLERY_CSS = r"""/* 100-Origin-Stories Gallery mobile filter chips & compact cards */
.pbp-orig-bar {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 0 0 14px;
}

.pbp-orig-top {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.pbp-orig-search-wrap {
  flex: 1 1 220px;
}

.pbp-orig-search {
  width: 100%;
  min-height: 40px;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid rgba(22, 35, 59, 0.22);
  background: var(--paper, #ffffff);
  color: inherit;
  font-size: 0.94rem;
}

.pbp-orig-random {
  min-height: 40px;
  padding: 6px 14px;
  border-radius: 8px;
  border: 1px solid #cc2f5a;
  background: #cc2f5a;
  color: #ffffff;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
}

.pbp-orig-chips {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  gap: 6px;
  padding: 2px 0 6px;
}

.pbp-orig-chip {
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

.pbp-orig-chip[aria-pressed="true"] {
  background: #16233b;
  color: #ffffff;
  border-color: #16233b;
}

.pbp-orig-cnt {
  opacity: 0.7;
  font-weight: 500;
  margin-left: 3px;
}

.pbp-orig-card {
  border: 1px solid rgba(22, 35, 59, 0.14);
  border-radius: 10px;
  background: var(--paper, #ffffff);
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.pbp-orig-head {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: baseline;
  gap: 6px;
}

.pbp-orig-title {
  margin: 0;
  font-size: 1rem;
}

.pbp-orig-cat-tag {
  font-size: 0.76rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(22, 35, 59, 0.08);
}

.pbp-orig-preview {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pbp-orig-more {
  margin-top: 4px;
  font-size: 0.86rem;
}

.pbp-orig-more > summary {
  cursor: pointer;
  font-weight: 600;
  color: #cc2f5a;
}

.pbp-orig-full {
  margin-top: 8px;
}
"""


def apply_patch(root: pathlib.Path) -> dict:
    js_dir = root / ".github" / "site-fixes" / "js"
    css_dir = root / ".github" / "site-fixes" / "css"
    js_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)

    changed: list[str] = []
    js_path = js_dir / "origins_gallery_ui.js"
    if not js_path.is_file() or js_path.read_text(encoding="utf-8") != ORIGINS_GALLERY_JS:
        js_path.write_text(ORIGINS_GALLERY_JS, encoding="utf-8")
        changed.append(str(js_path.relative_to(root)))

    css_path = css_dir / "origins_gallery_ui.css"
    if not css_path.is_file() or css_path.read_text(encoding="utf-8") != ORIGINS_GALLERY_CSS:
        css_path.write_text(ORIGINS_GALLERY_CSS, encoding="utf-8")
        changed.append(str(css_path.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        js_txt = (root / ".github" / "site-fixes" / "js" / "origins_gallery_ui.js").read_text(encoding="utf-8")
        css_txt = (root / ".github" / "site-fixes" / "css" / "origins_gallery_ui.css").read_text(encoding="utf-8")
        assert "renderOriginsFilterBar" in js_txt and "renderOriginStoryCard" in js_txt
        assert "MutationObserver" not in js_txt
        assert "var(--card" not in css_txt
        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("ORIGINS_GALLERY_MOBILE_CARDS_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage 100-Origin-Stories Gallery mobile filter chips & cards")
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
