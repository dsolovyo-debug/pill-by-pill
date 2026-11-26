#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch (Batch 3): Sticky Section Jump Bar & Mobile Back-to-Top Control.

Why:
  Long encyclopedia reference modules (24 entries across 4 pillars) and deep drug pages
  require heavy thumb scrolling on phones to switch pillars or return to the top search bar.

Fix:
  Stages a lightweight, zero-MutationObserver ES module `.github/site-fixes/js/section_toc.js`
  and companion stylesheet `.github/site-fixes/css/section_toc.css` exporting:
    - `renderSectionJumpBar(sections)`: sticky horizontal pill bar for 1-tap jumps between
      major page sections/pillars (scrolls smoothly and respects prefers-reduced-motion).
    - `attachSectionToc(container)`: wires smooth-scroll jump handlers and an unobtrusive
      floating `Top` pill button that appears only after scrolling past 480px.

Usage:
  python3 2026-11-26_sticky_mobile_back_to_top_and_section_toc_patch.py --selftest
  python3 2026-11-26_sticky_mobile_back_to_top_and_section_toc_patch.py --apply /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile

SECTION_TOC_JS = """// Sticky section jump bar & accessible Back-to-Top helper (zero MutationObserver)
import { html } from "./ui.js";

/**
 * Render a horizontal scrollable pill bar for jumping between page sections/pillars.
 * @param {Array<{id: string, label: string, count?: number}>} sections
 */
export function renderSectionJumpBar(sections) {
  const list = Array.isArray(sections) ? sections.filter((s) => s && s.id && s.label) : [];
  if (list.length < 2) return "";
  const items = list.map(
    (s) => html`<button type="button" class="toc-pill" data-toc-target="${s.id}">
      ${s.label}${typeof s.count === "number" ? html` <span class="toc-count">(${s.count})</span>` : ""}
    </button>`
  );
  return html`<nav class="pbp-toc-bar" aria-label="Jump to section">
    <div class="pbp-toc-scroll">${items}</div>
  </nav>`;
}

/**
 * Wire jump-bar click handlers and attach a single floating Back-to-Top button.
 * Returns a cleanup function suitable for app.js `view.mount()` lifecycle hooks.
 */
export function attachSectionToc(container) {
  if (!container) return () => {};
  const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const behavior = reduced ? "auto" : "smooth";

  container.querySelectorAll("[data-toc-target]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-toc-target");
      const target = id ? document.getElementById(id) : null;
      if (target) {
        target.scrollIntoView({ behavior, block: "start" });
      }
    });
  });

  let topBtn = document.getElementById("pbp-back-to-top");
  if (!topBtn) {
    topBtn = document.createElement("button");
    topBtn.id = "pbp-back-to-top";
    topBtn.type = "button";
    topBtn.className = "pbp-back-to-top";
    topBtn.setAttribute("aria-label", "Back to top");
    topBtn.textContent = "↑ Top";
    topBtn.hidden = true;
    topBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior });
    });
    document.body.appendChild(topBtn);
  }

  const onScroll = () => {
    topBtn.hidden = window.scrollY < 480;
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  return () => {
    window.removeEventListener("scroll", onScroll);
    if (topBtn) topBtn.hidden = true;
  };
}
"""

SECTION_TOC_CSS = """/* Sticky section jump bar & Back-to-Top button */
.pbp-toc-bar {
  position: sticky;
  top: 0;
  z-index: 20;
  background: var(--paper, #ffffff);
  border-bottom: 1px solid rgba(22, 35, 59, 0.12);
  margin: 0 -14px 12px;
  padding: 8px 14px;
}

.pbp-toc-scroll {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}

.pbp-toc-scroll::-webkit-scrollbar {
  display: none;
}

.toc-pill {
  flex: 0 0 auto;
  padding: 6px 11px;
  border-radius: 999px;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
  background: var(--paper, #ffffff);
  border: 1px solid rgba(22, 35, 59, 0.18);
  white-space: nowrap;
}

.toc-count {
  opacity: 0.65;
  font-weight: 500;
}

.pbp-back-to-top {
  position: fixed;
  right: 16px;
  bottom: calc(18px + env(safe-area-inset-bottom, 0px));
  z-index: 40;
  padding: 8px 13px;
  border-radius: 999px;
  font-size: 0.84rem;
  font-weight: 700;
  cursor: pointer;
  background: var(--paper, #ffffff);
  border: 1px solid rgba(22, 35, 59, 0.24);
  box-shadow: 0 3px 10px rgba(15, 23, 42, 0.14);
}
"""


def apply_patch(root: pathlib.Path) -> dict:
    js_dir = root / ".github" / "site-fixes" / "js"
    css_dir = root / ".github" / "site-fixes" / "css"
    js_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)

    changed: list[str] = []
    js_path = js_dir / "section_toc.js"
    if not js_path.is_file() or js_path.read_text(encoding="utf-8") != SECTION_TOC_JS:
        js_path.write_text(SECTION_TOC_JS, encoding="utf-8")
        changed.append(str(js_path.relative_to(root)))

    css_path = css_dir / "section_toc.css"
    if not css_path.is_file() or css_path.read_text(encoding="utf-8") != SECTION_TOC_CSS:
        css_path.write_text(SECTION_TOC_CSS, encoding="utf-8")
        changed.append(str(css_path.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        js_txt = (root / ".github" / "site-fixes" / "js" / "section_toc.js").read_text(encoding="utf-8")
        assert "renderSectionJumpBar" in js_txt
        assert "attachSectionToc" in js_txt
        assert "MutationObserver" not in js_txt
        css_txt = (root / ".github" / "site-fixes" / "css" / "section_toc.css").read_text(encoding="utf-8")
        assert "var(--card" not in css_txt

        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("STICKY_SECTION_TOC_BACK_TO_TOP_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage sticky section jump bar & Back-to-Top module")
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
