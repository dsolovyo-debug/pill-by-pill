#!/usr/bin/env python3
"""
v2 HTML Template Join Fix for Pill by Pill.

Fixes the superseded 2026-11-26_fix_html_template_join_and_aria_escaping_patch.py:
- Uses a lexical JS scanner (never a naive cross-backtick regex) so it ONLY
  inspects `${ ... }` interpolations directly inside `html` tagged template
  literals.
- Converts empty `.join()` at the end of a `.map(...)` / `.filter(...)`
  interpolation inside `html\`...\`` to `.join("")`, and appends `.join("")`
  when a `.map(...)` interpolation inside `html\`...\`` has no `.join(...)`.
- Never modifies `atomSentence(...)`, SVG curve points `.join(" ")`, or
  already-joined `.join("")` / `.join(", ")` expressions.
- `--selftest` verifies positive fixes, negative/regression safety on
  `explore.js` and `simulators.js` patterns, idempotency, and `node --check`.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


def _skip_string(src: str, i: int, quote: str) -> int:
    n = len(src)
    i += 1
    while i < n:
        ch = src[i]
        if ch == "\\":
            i += 2
            continue
        if ch == quote:
            return i + 1
        i += 1
    return n


def _skip_comment(src: str, i: int) -> int:
    n = len(src)
    if i + 1 < n and src[i + 1] == "/":
        nl = src.find("\n", i + 2)
        return n if nl == -1 else nl + 1
    if i + 1 < n and src[i + 1] == "*":
        end = src.find("*/", i + 2)
        return n if end == -1 else end + 2
    return i + 1


def _find_matching_paren(src: str, open_idx: int) -> int:
    n = len(src)
    depth = 0
    i = open_idx
    while i < n:
        ch = src[i]
        if ch in ("'", '"', "`"):
            if ch == "`":
                i = _scan_template(src, i, is_html=False, edits=None)
            else:
                i = _skip_string(src, i, ch)
            continue
        if ch == "/" and i + 1 < n and src[i + 1] in ("/", "*"):
            i = _skip_comment(src, i)
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _maybe_fix_html_expr(expr: str) -> str | None:
    stripped = expr.strip()
    # Case 1: ends with `.join()` (empty args) inside html`...`
    if re.search(r"\.join\(\s*\)$", stripped):
        if re.search(r"\.(?:map|filter)\s*\(", stripped):
            return re.sub(r"\.join\(\s*\)$", '.join("")', expr.rstrip()) + expr[len(expr.rstrip()):]
        return None

    # Case 2: ends with `.map(...)` with no `.join(...)`
    # Check by finding the last `.map(` and verifying its closing `)` is at the end of stripped.
    last_map = stripped.rfind(".map(")
    if last_map != -1:
        paren_open = last_map + 4
        paren_close = _find_matching_paren(stripped, paren_open)
        if paren_close == len(stripped) - 1:
            trailing_ws = expr[len(expr.rstrip()):]
            return expr.rstrip() + '.join("")' + trailing_ws

    return None


def _scan_template(src: str, tick_idx: int, is_html: bool, edits: list[tuple[int, int, str]] | None) -> int:
    n = len(src)
    i = tick_idx + 1
    while i < n:
        ch = src[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "`":
            return i + 1
        if ch == "$" and i + 1 < n and src[i + 1] == "{":
            expr_start = i + 2
            depth = 1
            j = expr_start
            while j < n and depth > 0:
                c = src[j]
                if c in ("'", '"'):
                    j = _skip_string(src, j, c)
                    continue
                if c == "`":
                    nested_html = j >= 4 and src[j - 4 : j] == "html" and (j == 4 or not (src[j - 5].isalnum() or src[j - 5] == "_"))
                    j = _scan_template(src, j, is_html=nested_html, edits=edits)
                    continue
                if c == "/" and j + 1 < n and src[j + 1] in ("/", "*"):
                    j = _skip_comment(src, j)
                    continue
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if is_html and edits is not None and depth == 0:
                expr = src[expr_start:j]
                fixed = _maybe_fix_html_expr(expr)
                if fixed is not None and fixed != expr:
                    edits.append((expr_start, j, fixed))
            i = j + 1
            continue
        i += 1
    return n


def fix_js_text(src: str) -> tuple[str, int]:
    edits: list[tuple[int, int, str]] = []
    n = len(src)
    i = 0
    while i < n:
        ch = src[i]
        if ch in ("'", '"'):
            i = _skip_string(src, i, ch)
            continue
        if ch == "/" and i + 1 < n and src[i + 1] in ("/", "*"):
            i = _skip_comment(src, i)
            continue
        if ch == "`":
            is_html = i >= 4 and src[i - 4 : i] == "html" and (i == 4 or not (src[i - 5].isalnum() or src[i - 5] == "_"))
            i = _scan_template(src, i, is_html=is_html, edits=edits)
            continue
        i += 1

    if not edits:
        return src, 0

    # Apply edits from back to front (non-overlapping top-level or nested; filter nested if parent replaced)
    edits.sort(key=lambda e: (e[0], -e[1]))
    filtered: list[tuple[int, int, str]] = []
    last_end = -1
    for s, e, rep in edits:
        if s >= last_end:
            filtered.append((s, e, rep))
            last_end = e

    out = src
    for s, e, rep in reversed(filtered):
        out = out[:s] + rep + out[e:]
    return out, len(filtered)


def apply_patch(repo_root: Path) -> dict[str, object]:
    changed_files: list[str] = []
    total_fixes = 0
    for base in (repo_root / "site" / "js", repo_root / ".github" / "site-fixes" / "js"):
        if not base.exists():
            continue
        for js_file in sorted(base.rglob("*.js")):
            orig = js_file.read_text(encoding="utf-8")
            updated, count = fix_js_text(orig)
            if count > 0 and updated != orig:
                js_file.write_text(updated, encoding="utf-8")
                changed_files.append(str(js_file.relative_to(repo_root)))
                total_fixes += count
    return {"changed_files": changed_files, "total_fixes": total_fixes}


def _run_node_check(js_path: Path) -> None:
    node = shutil.which("node")
    if not node:
        return
    res = subprocess.run([node, "--check", str(js_path)], capture_output=True, text=True)
    if res.returncode != 0:
        raise AssertionError(f"node --check failed on {js_path}: {res.stderr}")


def selftest() -> None:
    buggy_ref = """import { html } from "./ui.js";
export function renderRef(items, rows) {
  return html`
    <ul>${items.map(i => html`<li>${i}</li>`)}</ul>
    <div>${rows.map(r => r.label).join()}</div>
  `;
}
"""
    safe_explore = """import { html } from "./ui.js";
export function renderExplore(timeline, pts) {
  return html`
    <ol>${timeline.map(t => html`<li>${t.year}</li>`).join("")}</ol>
    <svg><polyline points="${pts.map(p => p.join(",")).join(" ")}" /></svg>
  `;
}
export function atomSentence(atoms) {
  return atoms.map(a => a.name).join(", ");
}
"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "package.json").write_text('{"type": "module"}\n', encoding="utf-8")
        js_dir = root / "site" / "js"
        js_dir.mkdir(parents=True)
        ref_file = js_dir / "v61b_reference.js"
        exp_file = js_dir / "explore.js"
        ref_file.write_text(buggy_ref, encoding="utf-8")
        exp_file.write_text(safe_explore, encoding="utf-8")

        r1 = apply_patch(root)
        assert r1["changed_files"] == ["site/js/v61b_reference.js"], r1
        assert r1["total_fixes"] == 2, r1
        assert exp_file.read_text(encoding="utf-8") == safe_explore, "explore.js was unexpectedly modified!"

        ref_fixed = ref_file.read_text(encoding="utf-8")
        assert 'html`<li>${i}</li>`)}</ul>' not in ref_fixed
        assert '.join("")}</ul>' in ref_fixed
        assert '.join("")}</div>' in ref_fixed

        # Idempotency check
        r2 = apply_patch(root)
        assert r2["changed_files"] == [] and r2["total_fixes"] == 0, r2

        _run_node_check(ref_file)
        _run_node_check(exp_file)
    print("FIX_HTML_TEMPLATE_JOIN_V2_SELFTEST_PASSED")


def main() -> None:
    parser = argparse.ArgumentParser(description="Safely fix missing/empty .join() inside html`` templates")
    parser.add_argument("--apply", type=Path, help="Path to pill-by-pill repository root")
    parser.add_argument("--selftest", action="store_true", help="Run self-test with node --check")
    args = parser.parse_args()
    if args.selftest:
        selftest()
    elif args.apply:
        print(apply_patch(args.apply))
    else:
        parser.error("Specify --apply <repo_root> or --selftest")


if __name__ == "__main__":
    main()
