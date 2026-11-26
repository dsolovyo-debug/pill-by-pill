#!/usr/bin/env python3
"""Fix double-escaped HTML (&quot;, &amp;quot;, &lt;a ...) and textContent assignments on Trace One Drug links."""
from __future__ import annotations

import html
import pathlib
import re
import sys


def _unescape_trace_html(text: str) -> str:
    prev = text
    for _ in range(3):
        nxt = html.unescape(prev)
        if nxt == prev:
            break
        prev = nxt
    return prev


def apply_patch(root: pathlib.Path) -> list[str]:
    changed: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in {".py", ".js", ".html"}:
            continue
        raw = path.read_text(encoding="utf-8", errors="ignore")
        if "Choose a medicine:" not in raw and "/ref/trace?drug=" not in raw:
            continue

        updated = raw
        if "&quot;" in updated or "&amp;quot;" in updated or "&lt;a " in updated:
            updated = re.sub(
                r"(Choose a medicine:\s*)([^\n<]+(?:&(?:amp;)?(?:lt|gt|quot);[^\n<]*)+)",
                lambda m: m.group(1) + _unescape_trace_html(m.group(2)),
                updated,
            )

        updated = re.sub(
            r"(\.textContent\s*=\s*`[^`]*?/ref/trace\?drug=[^`]*`)",
            lambda m: m.group(1).replace(".textContent", ".innerHTML", 1),
            updated,
        )

        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(root)))
    return changed


def main() -> int:
    target = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    files = apply_patch(target)
    print({"patched_files": files})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
