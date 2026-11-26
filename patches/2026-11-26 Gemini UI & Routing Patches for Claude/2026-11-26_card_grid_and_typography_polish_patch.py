#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch (Batch 3): Card Grid, Headings & Accordion Typography Polish.

Design note (aligned with Claude's .github/site-fixes/ architecture):
  Pure CSS — zero MutationObserver, zero inline <script> injection, zero deploy.yml edits.
  Appends an idempotent CSS block to `site/css/reference.css` and `site/css/explore.css`
  and stages a standalone copy at `.github/site-fixes/css/card_typography.css`.

Fixes:
  1. Responsive card grids: enforces `minmax(min(100%, 280px), 1fr)` on encyclopedia card
     grids so cards never crowd or cause horizontal overflow on 390px phone screens.
  2. Visual hierarchy & readable measure: constrains prose paragraphs to `68ch`, tightens
     heading margins (`h1`/`h2`/`h3`), and adds subtle card separation using `var(--paper, #ffffff)`
     (never undefined `var(--card)`) for light/dark mode consistency.
  3. Polished `<details>` / `<summary>` accordions: adds crisp chevron indicators, hover/focus
     rings, and clean internal spacing so collapsed encyclopedia sections look native.
  4. Compact metadata badges/tags: prevents badge walls from pushing content below the fold.

Usage:
  python3 2026-11-26_card_grid_and_typography_polish_patch.py --selftest
  python3 2026-11-26_card_grid_and_typography_polish_patch.py --apply /path/to/repo_or_site
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import tempfile

MARKER_START = "/* pbp-card-typography-v1:start */"
MARKER_END = "/* pbp-card-typography-v1:end */"

CARD_TYPOGRAPHY_CSS = f"""
{MARKER_START}
/* Readable measure & clean vertical rhythm */
main p,
main li {{
  max-width: 68ch;
  line-height: 1.55;
}}

main h1 {{
  letter-spacing: -0.02em;
  margin-bottom: 0.5rem;
}}

main h2 {{
  margin-top: 1.4rem;
  margin-bottom: 0.55rem;
  padding-bottom: 0.25rem;
  border-bottom: 1px solid rgba(22, 35, 59, 0.10);
}}

main h3 {{
  margin-top: 1rem;
  margin-bottom: 0.35rem;
}}

/* Responsive encyclopedia card grids */
.cards,
.card-grid,
.pillar-grid,
.dept-grid,
.ref-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
  gap: 12px;
  margin: 12px 0;
}}

.card,
.entry-card,
.pillar-card,
.dept-card {{
  background: var(--paper, #ffffff);
  border: 1px solid rgba(22, 35, 59, 0.14);
  border-radius: 12px;
  padding: 14px 16px;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}}

.card h3,
.entry-card h3,
.pillar-card h3,
.dept-card h3 {{
  margin-top: 0;
  font-size: 1.02rem;
  line-height: 1.3;
}}

/* Polished native <details> / <summary> accordions */
main details {{
  background: var(--paper, #ffffff);
  border: 1px solid rgba(22, 35, 59, 0.14);
  border-radius: 10px;
  padding: 10px 14px;
  margin: 10px 0;
}}

main details > summary {{
  cursor: pointer;
  font-weight: 600;
  list-style: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}}

main details > summary::-webkit-details-marker {{
  display: none;
}}

main details > summary::after {{
  content: "\\25BE";
  font-size: 0.9rem;
  opacity: 0.65;
  transition: transform 0.16s ease;
  flex-shrink: 0;
}}

main details[open] > summary::after {{
  transform: rotate(180deg);
}}

main details[open] > summary {{
  margin-bottom: 8px;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(22, 35, 59, 0.08);
}}

/* Compact badges & metadata pills */
.badge,
.tag,
.meta-pill {{
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 0.78rem;
  line-height: 1.35;
  font-weight: 600;
  border: 1px solid rgba(22, 35, 59, 0.14);
}}

@media (max-width: 640px) {{
  .card,
  .entry-card,
  .pillar-card,
  .dept-card {{
    padding: 12px 13px;
    border-radius: 10px;
  }}

  main details {{
    padding: 9px 11px;
  }}
}}
{MARKER_END}
""".lstrip("\n")


def _upsert_css_block(raw: str) -> str:
    if MARKER_START in raw and MARKER_END in raw:
        return re.sub(
            re.escape(MARKER_START) + r"[\s\S]*?" + re.escape(MARKER_END),
            CARD_TYPOGRAPHY_CSS.strip(),
            raw,
        )
    sep = "\n\n" if raw and not raw.endswith("\n\n") else ""
    return raw + sep + CARD_TYPOGRAPHY_CSS


def apply_patch(root: pathlib.Path) -> dict:
    changed: list[str] = []
    site_dir = root / "site" if (root / "site").is_dir() else root

    # 1. Stage standalone CSS in .github/site-fixes/css/ when applying to a repo root
    if (root / ".github").is_dir() or (root / "site").is_dir():
        fixes_css = root / ".github" / "site-fixes" / "css"
        fixes_css.mkdir(parents=True, exist_ok=True)
        staged = fixes_css / "card_typography.css"
        if not staged.is_file() or staged.read_text(encoding="utf-8") != CARD_TYPOGRAPHY_CSS:
            staged.write_text(CARD_TYPOGRAPHY_CSS, encoding="utf-8")
            changed.append(str(staged.relative_to(root)))

    # 2. Upsert into site/css/reference.css and site/css/explore.css when present
    for css_name in ("reference.css", "explore.css"):
        css_path = site_dir / "css" / css_name
        if css_path.is_file():
            raw = css_path.read_text(encoding="utf-8", errors="ignore")
            updated = _upsert_css_block(raw)
            if updated != raw:
                css_path.write_text(updated, encoding="utf-8")
                changed.append(str(css_path.relative_to(root)))

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
        ref_txt = (css_dir / "reference.css").read_text(encoding="utf-8")
        assert MARKER_START in ref_txt and "var(--card" not in ref_txt

        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("CARD_GRID_TYPOGRAPHY_POLISH_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply card grid, heading & accordion typography polish")
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
