#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch (Batch 4): Compare & Data Sets Sticky First-Column & Mobile Cards CSS.

Why:
  Side-by-side medicine comparison tables and the Data Sets download view can become hard
  to read on narrow phones when swiping horizontally loses the row label, or when download
  action buttons crowd together.

Fix:
  Pure CSS (zero JS, zero MutationObserver, zero `var(--card)`):
    1. Stages `.github/site-fixes/css/compare_datasets_mobile.css` AND idempotently appends
       to `site/css/reference.css` and `site/css/explore.css` when present.
    2. Pins the first column (`th:first-child`, `td:first-child`) on `.compare-table` /
       `[data-compare-table]` so row labels stay visible during horizontal touch-scroll.
    3. Gives dataset download/export cards clean responsive grids and >= 40px touch buttons.

Usage:
  python3 2026-11-26_compare_and_datasets_mobile_cards_patch.py --selftest
  python3 2026-11-26_compare_and_datasets_mobile_cards_patch.py --apply /path/to/repo_or_site
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import tempfile

MARKER_START = "/* pbp-compare-datasets-mobile-v1:start */"
MARKER_END = "/* pbp-compare-datasets-mobile-v1:end */"

CSS_BLOCK = f"""{MARKER_START}
/* Sticky first-column labels on horizontal comparison tables */
.compare-table th:first-child,
.compare-table td:first-child,
[data-compare-table] th:first-child,
[data-compare-table] td:first-child {{
  position: sticky;
  left: 0;
  z-index: 2;
  background: var(--paper, #ffffff);
  box-shadow: 1px 0 0 rgba(22, 35, 59, 0.12);
  font-weight: 600;
}}

/* Clean responsive dataset & export card grid */
.dataset-grid,
.datasets-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 270px), 1fr));
  gap: 12px;
}}

.dataset-card .actions,
.dataset-actions {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}}

.dataset-card .actions a,
.dataset-card .actions button,
.dataset-actions a,
.dataset-actions button {{
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 8px;
}}
{MARKER_END}
"""


def _upsert(raw: str) -> str:
    if MARKER_START in raw and MARKER_END in raw:
        return re.sub(
            re.escape(MARKER_START) + r"[\s\S]*?" + re.escape(MARKER_END),
            CSS_BLOCK.strip(),
            raw,
        )
    sep = "\n\n" if raw and not raw.endswith("\n\n") else ""
    return raw + sep + CSS_BLOCK


def apply_patch(root: pathlib.Path) -> dict:
    changed: list[str] = []

    sf_css_dir = root / ".github" / "site-fixes" / "css"
    sf_css_dir.mkdir(parents=True, exist_ok=True)
    sf_css = sf_css_dir / "compare_datasets_mobile.css"
    if not sf_css.is_file() or sf_css.read_text(encoding="utf-8") != CSS_BLOCK:
        sf_css.write_text(CSS_BLOCK, encoding="utf-8")
        changed.append(str(sf_css.relative_to(root)))

    site_dir = root / "site" if (root / "site").is_dir() else root
    for name in ("reference.css", "explore.css"):
        p = site_dir / "css" / name
        if p.is_file():
            raw = p.read_text(encoding="utf-8", errors="ignore")
            upd = _upsert(raw)
            if upd != raw:
                p.write_text(upd, encoding="utf-8")
                changed.append(str(p.relative_to(root)))

    return {"patched_files": sorted(set(changed)), "count": len(set(changed))}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        css_dir = root / "site" / "css"
        css_dir.mkdir(parents=True)
        (css_dir / "reference.css").write_text("body { margin: 0; }\n", encoding="utf-8")
        (css_dir / "explore.css").write_text("body { margin: 0; }\n", encoding="utf-8")

        r1 = apply_patch(root)
        assert r1["count"] == 3, r1
        assert "var(--card" not in (root / ".github" / "site-fixes" / "css" / "compare_datasets_mobile.css").read_text(encoding="utf-8")

        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("COMPARE_AND_DATASETS_MOBILE_CARDS_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage Compare & Data Sets sticky-column and mobile cards CSS")
    ap.add_argument("--apply", type=pathlib.Path, help="Path to repo or site root")
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
