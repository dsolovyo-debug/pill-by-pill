#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch: Eliminate double-escaped HTML from `html` template `.join()`
calls and interpolated `aria-current="page"` strings across all `site/js/*.js` modules.

Root cause confirmed in `site/js/v61b_reference.js` (Trace One Drug & Glossary):
  1. `list.map((s) => html`<a ...>...</a>`).join(" · ")` coerces SafeHTML objects into a
     plain string, which the outer `html` tagged template then HTML-escapes into literal
     `<a href=...>` text on screen.
  2. `${cond ? ' aria-current="page"' : ""}` inside `html` escapes quotes into
     `aria-current=&quot;page&quot;`.

Usage:
  python3 2026-11-26_fix_html_template_join_and_aria_escaping_patch.py --selftest
  python3 2026-11-26_fix_html_template_join_and_aria_escaping_patch.py --apply /path/to/site_or_source
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import tempfile


def _fix_js_source(txt: str) -> str:
    out = txt

    # 1. Fix interpolated aria-current attribute strings inside html`` templates:
    #    ${cond ? ' aria-current="page"' : ""}  ->  aria-current="${cond ? "page" : "false"}"
    out = re.sub(
        r'\$\{([^}]+?)\s*\?\s*(?:\'\s*aria-current="page"\'|"\s*aria-current=\'page\'")\s*:\s*(?:""|\'\')\s*\}',
        lambda m: f' aria-current="${{{m.group(1).strip()} ? "page" : "false"}}"',
        out,
    )

    # 2. Fix .map((x) => html`...`).join("sep") which coerces SafeHTML to plain string
    #    Convert to .map((x, _pbpIdx) => html`${_pbpIdx ? "sep" : ""}...`)
    map_join_re = re.compile(
        r'\.map\(\s*\(([A-Za-z_$][\w$]*)\)\s*=>\s*html`([\s\S]*?)`\s*\)\.join\(\s*(["\'])([^"\']*)\3\s*\)'
    )

    def _replace_map_join(m: re.Match) -> str:
        param, body, quote, sep = m.group(1), m.group(2), m.group(3), m.group(4)
        return f'.map(({param}, _pbpIdx) => html`${{_pbpIdx ? {quote}{sep}{quote} : ""}}{body}`)'

    out = map_join_re.sub(_replace_map_join, out)

    # 3. Also handle single-param arrow without parens: .map(x => html`...`).join("sep")
    map_join_bare_re = re.compile(
        r'\.map\(\s*([A-Za-z_$][\w$]*)\s*=>\s*html`([\s\S]*?)`\s*\)\.join\(\s*(["\'])([^"\']*)\3\s*\)'
    )
    out = map_join_bare_re.sub(_replace_map_join, out)

    return out


def apply_patch(root: pathlib.Path) -> dict:
    changed = []
    search_dir = root / "site" / "js" if (root / "site" / "js").is_dir() else root
    for js_file in sorted(search_dir.rglob("*.js")):
        if not js_file.is_file():
            continue
        raw = js_file.read_text(encoding="utf-8", errors="ignore")
        updated = _fix_js_source(raw)
        if updated != raw:
            js_file.write_text(updated, encoding="utf-8")
            changed.append(str(js_file.relative_to(root)))
    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    sample = (
        'import { html } from "./ui.js";\n'
        'export function trace(list, active, base) {\n'
        '  return html`<p>Choose a medicine:\n'
        '    ${list.map((s) => html`<a href="${base}?drug=${s.id}"${s.id === active.id ? \' aria-current="page"\' : ""}><b>${s.drug_name}</b></a>`).join(" · ")}\n'
        '  </p><p>Sources: ${active.sources.map((src) => html`<a href="${src.url}">${src.label}</a>`).join(" · ")}</p>`;\n'
        '}\n'
    )
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        js_dir = root / "site" / "js"
        js_dir.mkdir(parents=True)
        target = js_dir / "v61b_reference.js"
        target.write_text(sample, encoding="utf-8")

        r1 = apply_patch(root)
        assert r1["count"] == 1, r1
        fixed = target.read_text(encoding="utf-8")
        assert '.join(" · ")' not in fixed, fixed
        assert '\' aria-current="page"\'' not in fixed, fixed
        assert 'aria-current="${s.id === active.id ? "page" : "false"}"' in fixed, fixed
        assert '_pbpIdx ? " · " : ""' in fixed, fixed

        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
    print("FIX_HTML_TEMPLATE_JOIN_ARIA_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Fix html`` .join() and aria-current escaping bugs in site/js/*.js")
    ap.add_argument("--apply", type=pathlib.Path, help="Path to repo/source/site root")
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
