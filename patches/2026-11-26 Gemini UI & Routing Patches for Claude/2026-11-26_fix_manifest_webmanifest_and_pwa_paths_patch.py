#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch: Fix manifest.webmanifest 404 & subpath-safe PWA paths.

Why:
  Live GitHub Pages console logs repeated 404 errors on every page load:
    GET https://dsolovyo-debug.github.io/pill-by-pill/manifest.webmanifest 404 (Not Found)
  Because the site is served under a project subpath (/pill-by-pill/), any missing
  manifest file or root-relative start_url/icon path triggers console errors.

Fix:
  1. Ensures `site/manifest.webmanifest` exists with subpath-safe relative paths
     (`start_url: "./"`, `scope: "./"`, relative `img/...` icon paths when present).
  2. Rewrites root-relative `start_url`, `scope`, or icon `src` values in an existing
     `manifest.webmanifest` to relative paths so it works identically on Netlify and
     GitHub Pages project subpaths.
  3. Ensures `site/index.html` references `href="manifest.webmanifest"` (relative) rather
     than `/manifest.webmanifest`.

Usage:
  python3 2026-11-26_fix_manifest_webmanifest_and_pwa_paths_patch.py --selftest
  python3 2026-11-26_fix_manifest_webmanifest_and_pwa_paths_patch.py --apply /path/to/repo_or_site
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import tempfile

DEFAULT_MANIFEST = {
    "name": "Pill by Pill — The story of the world's medicines",
    "short_name": "Pill by Pill",
    "description": "Free, no-tracking explorer of approved medicines, 3D binding sites, drug development, and global regulation.",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": "#faf8f5",
    "theme_color": "#16233b",
    "icons": [],
}


def _discover_icons(site_dir: pathlib.Path) -> list[dict]:
    icons: list[dict] = []
    candidates = [
        ("img/icon-192.png", "192x192", "image/png"),
        ("img/icon-512.png", "512x512", "image/png"),
        ("img/favicon.svg", "any", "image/svg+xml"),
        ("favicon.svg", "any", "image/svg+xml"),
    ]
    for rel, sizes, mime in candidates:
        if (site_dir / rel).is_file():
            icons.append({"src": rel, "sizes": sizes, "type": mime})
    return icons


def _normalize_manifest(data: dict, site_dir: pathlib.Path) -> dict:
    out = dict(DEFAULT_MANIFEST)
    out.update(data)
    out["start_url"] = "./"
    out["scope"] = "./"
    norm_icons = []
    for ic in out.get("icons") or []:
        if not isinstance(ic, dict) or not ic.get("src"):
            continue
        src = str(ic["src"]).lstrip("/")
        if src.startswith("pill-by-pill/"):
            src = src[len("pill-by-pill/"):]
        if (site_dir / src).is_file():
            entry = dict(ic)
            entry["src"] = src
            norm_icons.append(entry)
    if not norm_icons:
        norm_icons = _discover_icons(site_dir)
    out["icons"] = norm_icons
    return out


def apply_patch(root: pathlib.Path) -> dict:
    site_dir = root / "site" if (root / "site").is_dir() else root
    changed: list[str] = []

    manifest_path = site_dir / "manifest.webmanifest"
    existing_data: dict = {}
    old_txt = ""
    if manifest_path.is_file():
        old_txt = manifest_path.read_text(encoding="utf-8", errors="ignore")
        try:
            existing_data = json.loads(old_txt)
        except json.JSONDecodeError:
            existing_data = {}

    new_data = _normalize_manifest(existing_data, site_dir)
    new_txt = json.dumps(new_data, indent=2) + "\n"
    if new_txt != old_txt:
        manifest_path.write_text(new_txt, encoding="utf-8")
        changed.append(str(manifest_path.relative_to(root)))

    index_html = site_dir / "index.html"
    if index_html.is_file():
        raw = index_html.read_text(encoding="utf-8", errors="ignore")
        updated = re.sub(
            r'(<link\b[^>]*\brel=["\']manifest["\'][^>]*\bhref=["\'])(?:/pill-by-pill/|/)?manifest\.webmanifest(["\'])',
            r'\1manifest.webmanifest\2',
            raw,
            flags=re.IGNORECASE,
        )
        if updated != raw:
            index_html.write_text(updated, encoding="utf-8")
            changed.append(str(index_html.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        site = root / "site"
        (site / "img").mkdir(parents=True)
        (site / "img" / "icon-192.png").write_bytes(b"png")
        (site / "index.html").write_text(
            '<!doctype html><html><head><link rel="manifest" href="/manifest.webmanifest"></head><body></body></html>\n',
            encoding="utf-8",
        )

        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        m = json.loads((site / "manifest.webmanifest").read_text(encoding="utf-8"))
        assert m["start_url"] == "./" and m["scope"] == "./", m
        assert m["icons"] == [{"src": "img/icon-192.png", "sizes": "192x192", "type": "image/png"}], m
        assert 'href="manifest.webmanifest"' in (site / "index.html").read_text(encoding="utf-8")

        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("FIX_MANIFEST_WEBMANIFEST_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Fix manifest.webmanifest 404 & subpath-safe PWA paths")
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
