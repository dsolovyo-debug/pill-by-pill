#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch: Mobile Header, Responsive Tables/SVGs & Dark-Mode CSS Polish.

Design note (per Claude's 2026-11-26 08:20 ET feedback):
  Pure CSS + static file hygiene — zero MutationObserver, zero inline <script> injection.
  Designed to be appended into `site/css/reference.css` and `site/css/explore.css` (or
  staged in `.github/site-fixes/css/` and appended by `prepare_pages.py`).

Fixes:
  1. Mobile header breathing room: prevents top-edge clipping of "Pill by Pill REFERENCE"
     on mobile browsers and tightens vertical padding so content starts higher on 390px screens.
  2. Responsive SVGs & wide comparison tables: ensures all inline encyclopedia SVGs scale
     smoothly (`max-width: 100%; height: auto`) and wide data tables scroll horizontally
     inside their container without causing page-wide sideways scroll.
  3. Touch-friendly filter chips & buttons: enforces comfortable tap targets with
     clean wrapping on small viewports.
  4. Replaces any leftover undefined `var(--card)` CSS references with `var(--paper, #ffffff)`
     so dark mode never renders white-on-white cards.

Usage:
  python3 2026-11-26_mobile_tables_svgs_and_header_polish_patch.py --selftest
  python3 2026-11-26_mobile_tables_svgs_and_header_polish_patch.py --apply /path/to/repo_or_site
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import tempfile

MARKER_START = "/* pbp-mobile-polish-v1:start */"
MARKER_END = "/* pbp-mobile-polish-v1:end */"

POLISH_CSS = f"""
{MARKER_START}
/* Responsive inline SVGs across all encyclopedia modules */
main svg {{
  max-width: 100%;
  height: auto;
  display: block;
}}

/* Prevent wide encyclopedia tables from causing page-level horizontal overflow */
main table {{
  display: block;
  max-width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  border-collapse: collapse;
}}

/* Comfortable filter-bar wrapping */
.filters,
.filter-bar,
.chip-row,
.pill-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}}

@media (max-width: 640px) {{
  header,
  .ref-header,
  .x-header {{
    padding-top: max(10px, env(safe-area-inset-top, 10px));
    padding-bottom: 10px;
  }}

  main {{
    padding-left: 14px;
    padding-right: 14px;
    overflow-wrap: anywhere;
  }}

  main h1 {{
    font-size: clamp(1.45rem, 6vw, 1.85rem);
    line-height: 1.18;
    margin-top: 0.4rem;
  }}

  main h2 {{
    font-size: clamp(1.15rem, 4.6vw, 1.35rem);
    line-height: 1.25;
  }}

  main table th,
  main table td {{
    padding: 8px 10px;
    font-size: 0.88rem;
  }}

  .filters button,
  .filter-bar button,
  .chip-row button,
  .pill-row button {{
    min-height: 38px;
    padding: 6px 11px;
    font-size: 0.86rem;
  }}
}}
{MARKER_END}
""".lstrip("\n")


def _upsert_css_block(raw: str) -> str:
    if MARKER_START in raw and MARKER_END in raw:
        return re.sub(
            re.escape(MARKER_START) + r"[\s\S]*?" + re.escape(MARKER_END),
            POLISH_CSS.strip(),
            raw,
        )
    sep = "\n\n" if raw and not raw.endswith("\n\n") else ""
    return raw + sep + POLISH_CSS


def apply_patch(root: pathlib.Path) -> dict:
    changed: list[str] = []
    site_dir = root / "site" if (root / "site").is_dir() else root

    for css_name in ("reference.css", "explore.css"):
        css_path = site_dir / "css" / css_name
        if css_path.is_file():
            raw = css_path.read_text(encoding="utf-8", errors="ignore")
            updated = _upsert_css_block(raw)
            updated = re.sub(r"var\(--card(?:\s*,\s*[^)]+)?\)", "var(--paper, #ffffff)", updated)
            if updated != raw:
                css_path.write_text(updated, encoding="utf-8")
                changed.append(str(css_path.relative_to(root)))

    for ext in ("*.css", "*.js"):
        for p in sorted(site_dir.rglob(ext)):
            if not p.is_file():
                continue
            raw = p.read_text(encoding="utf-8", errors="ignore")
            if "var(--card" not in raw:
                continue
            updated = re.sub(r"var\(--card(?:\s*,\s*[^)]+)?\)", "var(--paper, #ffffff)", raw)
            if updated != raw:
                p.write_text(updated, encoding="utf-8")
                changed.append(str(p.relative_to(root)))

    return {"patched_files": sorted(set(changed)), "count": len(set(changed))}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        css_dir = root / "site" / "css"
        js_dir = root / "site" / "js"
        css_dir.mkdir(parents=True)
        js_dir.mkdir(parents=True)
        (css_dir / "reference.css").write_text(".box { background: var(--card, #fff); }\n", encoding="utf-8")
        (css_dir / "explore.css").write_text("body { margin: 0; }\n", encoding="utf-8")
        (js_dir / "sample.js").write_text('const s = "background: var(--card)";\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert r1["count"] == 3, r1
        ref_txt = (css_dir / "reference.css").read_text(encoding="utf-8")
        assert "var(--card" not in ref_txt and MARKER_START in ref_txt
        assert "var(--card" not in (js_dir / "sample.js").read_text(encoding="utf-8")

        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("MOBILE_TABLES_SVGS_HEADER_POLISH_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply mobile header, table, SVG & CSS polish")
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
