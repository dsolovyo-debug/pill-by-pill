#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch: Remove user-agent-conditional JS redirects from static SEO
encyclopedia pages (addresses Claude's 2026-11-25 SEO/cloaking warning).

Why:
  `pipeline/build_v60_static_pages.py` currently injects:
    <script>if (!/bot|crawl|spider|slurp|bingpreview/i.test(navigator.userAgent)) { location.replace(...); }</script>
  Serving static HTML to crawlers while redirecting human browsers via User-Agent sniffing
  can be flagged by Google Search Console as a sneaky redirect / cloaking.

Fix:
  Removes the UA-sniffing redirect script from `pipeline/build_v60_static_pages.py` (and any
  already-built static HTML pages) and adds clean, lightweight CSS + a prominent
  "Open interactive view in Pill by Pill ->" call-to-action button so crawlers and humans
  see identical, readable content.

Usage:
  python3 2026-11-26_fix_static_seo_cloaking_redirect_patch.py --selftest
  python3 2026-11-26_fix_static_seo_cloaking_redirect_patch.py --apply /path/to/repo_or_source
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import tempfile

STATIC_STYLE = (
    '<style>'
    'body{font-family:system-ui,-apple-system,sans-serif;max-width:760px;margin:0 auto;padding:24px 16px;line-height:1.55;color:#16233b;background:#faf8f5}'
    'a{color:#b4234d}a.pbp-cta{display:inline-block;margin:12px 0;padding:10px 16px;border-radius:999px;background:#b4234d;color:#fff;text-decoration:none;font-weight:600}'
    '</style>'
)

UA_REDIRECT_PY_RE = re.compile(
    r"""^\s*f?['"]\s*<script>if \(!/bot\|crawl\|spider\|slurp\|bingpreview/i\.test\(navigator\.userAgent\)\)[^\n]*</script>\\n['"]\s*\n""",
    re.MULTILINE,
)

UA_REDIRECT_HTML_RE = re.compile(
    r"""\s*<script>\s*if\s*\(!/bot\|crawl\|spider\|slurp\|bingpreview/i\.test\(navigator\.userAgent\)\)[^<]*</script>\s*""",
    re.IGNORECASE,
)


def apply_patch(root: pathlib.Path) -> dict:
    changed = []

    # 1. Patch pipeline/build_v60_static_pages.py if present
    builder = root / "pipeline" / "build_v60_static_pages.py"
    if builder.is_file():
        raw = builder.read_text(encoding="utf-8", errors="ignore")
        updated = UA_REDIRECT_PY_RE.sub(f"        '{STATIC_STYLE}\\n'\n", raw)
        updated = updated.replace(
            '<a href="/{_esc(hash_route)}">Open interactive view in Pill by Pill</a>',
            '<a class="pbp-cta" href="/{_esc(hash_route)}">Open interactive view in Pill by Pill &rarr;</a>',
        )
        if updated != raw:
            builder.write_text(updated, encoding="utf-8")
            changed.append(str(builder.relative_to(root)))

    # 2. Also strip UA redirects from any already-built static HTML pages under site/
    site_dir = root / "site" if (root / "site").is_dir() else root
    for html_file in sorted(site_dir.rglob("index.html")):
        if html_file == site_dir / "index.html":
            continue
        raw = html_file.read_text(encoding="utf-8", errors="ignore")
        if "navigator.userAgent" not in raw or "location.replace" not in raw:
            continue
        updated = UA_REDIRECT_HTML_RE.sub(f"\n  {STATIC_STYLE}\n", raw)
        if updated != raw:
            html_file.write_text(updated, encoding="utf-8")
            changed.append(str(html_file.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    sample_py = (
        'def _render_page(hash_route):\n'
        '    return (\n'
        '        \'  <script type="application/ld+json">{}</script>\\n\'\n'
        '        f\'  <script>if (!/bot|crawl|spider|slurp|bingpreview/i.test(navigator.userAgent)) {{ location.replace("/{_esc(hash_route)}"); }}</script>\\n\'\n'
        '        "</head><body>"\n'
        '        f\'    <p><a href="/{_esc(hash_route)}">Open interactive view in Pill by Pill</a></p>\\n\'\n'
        '    )\n'
    )
    sample_html = (
        '<!doctype html><html><head>\n'
        '  <script>if (!/bot|crawl|spider|slurp|bingpreview/i.test(navigator.userAgent)) { location.replace("/pill-by-pill/#/ref/trace"); }</script>\n'
        '</head><body><main><h1>Trace</h1></main></body></html>\n'
    )
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "trace").mkdir(parents=True)
        b = root / "pipeline" / "build_v60_static_pages.py"
        h = root / "site" / "trace" / "index.html"
        b.write_text(sample_py, encoding="utf-8")
        h.write_text(sample_html, encoding="utf-8")

        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        assert "navigator.userAgent" not in b.read_text(encoding="utf-8")
        assert "navigator.userAgent" not in h.read_text(encoding="utf-8")
        assert "pbp-cta" in b.read_text(encoding="utf-8")

        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
    print("FIX_STATIC_SEO_CLOAKING_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Remove UA-conditional redirects from static SEO pages")
    ap.add_argument("--apply", type=pathlib.Path, help="Path to repo/source root")
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
