#!/usr/bin/env python3
"""
v2 Card Grid & Typography Polish Patch for Pill by Pill.

Fixes the superseded 2026-11-26_card_grid_and_typography_polish_patch.py:
- Uses a lambda replacement (`lambda _m: CSS_BLOCK`) in `re.sub` so `\\25BE`
  inside the CSS `content` property never raises `re.PatternError: invalid
  group reference 25` on re-runs.
- `--selftest` runs `--apply` twice on mock `reference.css` and `explore.css`
  files to verify idempotency.
"""

from __future__ import annotations

import argparse
import re
import tempfile
from pathlib import Path

MARKER = "/* v6-card-grid-typography-polish */"

CSS_BLOCK = """/* v6-card-grid-typography-polish */
main h1 { font-size: clamp(1.55rem, 3.2vw, 2.15rem); line-height: 1.22; letter-spacing: -0.015em; }
main h2 { font-size: clamp(1.2rem, 2.4vw, 1.55rem); line-height: 1.28; margin-top: 1.75rem; }
main h3 { font-size: clamp(1.02rem, 1.9vw, 1.2rem); line-height: 1.35; }
main p, main li { line-height: 1.62; max-width: 72ch; }
main details summary { cursor: pointer; font-weight: 600; list-style: none; }
main details summary::before { content: "\\25B8\\00A0"; display: inline-block; transition: transform 0.15s ease; }
main details[open] summary::before { content: "\\25BE\\00A0"; }
@media (max-width: 640px) {
  .card-grid, .ref-grid, .topic-grid { grid-template-columns: 1fr !important; gap: 0.85rem; }
}
/* /v6-card-grid-typography-polish */"""

BLOCK_RE = re.compile(
    r"/\*\s*v6-card-grid-typography-polish\s*\*/[\s\S]*?/\*\s*/v6-card-grid-typography-polish\s*\*/",
    re.MULTILINE,
)


def patch_css_file(path: Path) -> bool:
    if not path.exists():
        return False
    orig = path.read_text(encoding="utf-8")
    if BLOCK_RE.search(orig):
        updated = BLOCK_RE.sub(lambda _m: CSS_BLOCK, orig, count=1)
    else:
        sep = "" if (not orig or orig.endswith("\n")) else "\n"
        updated = orig + sep + "\n" + CSS_BLOCK + "\n"
    if updated == orig:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def apply_patch(repo_root: Path) -> dict[str, list[str]]:
    targets = [
        repo_root / "site" / "css" / "reference.css",
        repo_root / "site" / "css" / "explore.css",
        repo_root / ".github" / "site-fixes" / "css" / "reference.css",
        repo_root / ".github" / "site-fixes" / "css" / "explore.css",
    ]
    changed: list[str] = []
    for t in targets:
        if patch_css_file(t):
            changed.append(str(t.relative_to(repo_root)))
    return {"changed": changed}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        css_dir = root / "site" / "css"
        css_dir.mkdir(parents=True)
        ref_css = css_dir / "reference.css"
        exp_css = css_dir / "explore.css"
        ref_css.write_text("body { margin: 0; }\n", encoding="utf-8")
        exp_css.write_text("main { padding: 1rem; }\n", encoding="utf-8")

        r1 = apply_patch(root)
        assert len(r1["changed"]) == 2, r1
        # Second run must succeed without re.PatternError and be idempotent
        r2 = apply_patch(root)
        assert r2["changed"] == [], r2
        assert "\\25BE" in ref_css.read_text(encoding="utf-8")
    print("CARD_GRID_AND_TYPOGRAPHY_POLISH_V2_SELFTEST_PASSED")


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply card grid and typography polish CSS safely")
    parser.add_argument("--apply", type=Path, help="Path to pill-by-pill repository root")
    parser.add_argument("--selftest", action="store_true", help="Run idempotency self-test")
    args = parser.parse_args()
    if args.selftest:
        selftest()
    elif args.apply:
        print(apply_patch(args.apply))
    else:
        parser.error("Specify --apply <repo_root> or --selftest")


if __name__ == "__main__":
    main()
