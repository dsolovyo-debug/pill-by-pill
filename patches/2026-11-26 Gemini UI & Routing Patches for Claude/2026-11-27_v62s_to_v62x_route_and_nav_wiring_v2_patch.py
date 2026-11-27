#!/usr/bin/env python3
"""
v2 Route & Nav Wiring Patch for Pill by Pill modules v6.2s - v6.2x.

Fixes the superseded 2026-11-26_v62s_to_v62v_route_and_nav_wiring_patch.py:
- Inserts all 6 modules (v6.2s-v6.2x) into `export const ROUTES = { ... };`
  in `.github/site-fixes/js/v6_routes.js` using `M(file, fn, { args: "c" })`,
  never into `v6Route()`.
- Updates `.github/site-fixes/js/ref_nav.js` (when present) to place each of
  the 6 slugs into its target sidebar section.
- `--selftest` runs `--apply` twice on realistic `v6_routes.js` + `ref_nav.js`
  fixtures and verifies syntax with `node --check`.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

MODULES = [
    ("discovery-sbdd-protacs", "discovery_sbdd_protacs.js", "discoverySbddProtacsPage", "Science & modalities"),
    ("packaging-el-dscsa", "packaging_el_dscsa.js", "packagingElDscsaPage", "Manufacturing & quality"),
    ("user-fees-prv", "user_fees_prv.js", "userFeesPrvPage", "Regulatory & policy"),
    ("pv-faers-sentinel", "pv_faers_sentinel.js", "pvFaersSentinelPage", "Clinical & safety"),
    ("microbiology-sterility", "microbiology_sterility.js", "microbiologySterilityPage", "Manufacturing & quality"),
    ("dmepa-med-errors", "dmepa_med_errors.js", "dmepaMedErrorsPage", "Clinical & safety"),
]


def _find_matching_brace(text: str, open_idx: int) -> int:
    depth = 0
    in_str: str | None = None
    escaped = False
    i = open_idx
    n = len(text)
    while i < n:
        ch = text[i]
        if in_str:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_str:
                in_str = None
        else:
            if ch in ("'", '"', "`"):
                in_str = ch
            elif ch == "/" and i + 1 < n and text[i + 1] == "/":
                nl = text.find("\n", i)
                i = n if nl == -1 else nl
            elif ch == "/" and i + 1 < n and text[i + 1] == "*":
                end = text.find("*/", i + 2)
                i = n if end == -1 else end + 1
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    raise ValueError("Unclosed '{' in JS file")


def patch_v6_routes(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"\bexport\s+const\s+ROUTES\s*=\s*\{", text)
    if not m:
        raise RuntimeError(f"Could not find `export const ROUTES = {{` in {path}")
    open_brace = m.end() - 1
    close_brace = _find_matching_brace(text, open_brace)
    routes_body = text[open_brace + 1 : close_brace]

    added: list[str] = []
    new_lines: list[str] = []
    for slug, js_file, fn_name, _section in MODULES:
        if re.search(rf'["\']{re.escape(slug)}["\']\s*:', routes_body):
            continue
        new_lines.append(f'  "{slug}": M("{js_file}", "{fn_name}", {{ args: "c" }}),')
        added.append(slug)

    if not added:
        return False, []

    prefix = text[:close_brace]
    # Ensure trailing comma / newline before inserting new entries
    stripped = prefix.rstrip()
    if stripped and not stripped.endswith("{") and not stripped.endswith(","):
        prefix = stripped + ",\n"
    elif not prefix.endswith("\n"):
        prefix = prefix + "\n"

    updated = prefix + "\n".join(new_lines) + "\n" + text[close_brace:]
    path.write_text(updated, encoding="utf-8")
    return True, added


def patch_ref_nav(path: Path) -> tuple[bool, list[str]]:
    if not path.exists():
        return False, []
    text = path.read_text(encoding="utf-8")
    added: list[str] = []

    for slug, _js_file, _fn_name, section in MODULES:
        if re.search(rf'["\']{re.escape(slug)}["\']', text):
            continue
        # Locate section title string, then find the next `[` ... `]` array
        sec_pat = re.compile(rf'["\']{re.escape(section)}["\']')
        sm = sec_pat.search(text)
        if not sm:
            continue
        arr_start = text.find("[", sm.end())
        if arr_start == -1:
            continue
        arr_end = text.find("]", arr_start)
        if arr_end == -1:
            continue
        arr_inner = text[arr_start + 1 : arr_end]
        if "\n" in arr_inner:
            # Multi-line array
            before = text[:arr_end].rstrip()
            if before and not before.endswith("[") and not before.endswith(","):
                before += ","
            indent_match = re.search(r"\n([ \t]+)[\"']", arr_inner)
            indent = indent_match.group(1) if indent_match else "      "
            text = before + f'\n{indent}"{slug}",\n' + text[arr_end:].lstrip("\n")
        else:
            # Single-line array
            before = text[:arr_end].rstrip()
            if before and not before.endswith("[") and not before.endswith(","):
                before += ", "
            text = before + f'"{slug}"' + text[arr_end:]
        added.append(slug)

    if added:
        path.write_text(text, encoding="utf-8")
    return bool(added), added


def apply_patch(repo_root: Path) -> dict[str, object]:
    routes_path = repo_root / ".github" / "site-fixes" / "js" / "v6_routes.js"
    if not routes_path.exists():
        raise FileNotFoundError(f"Missing {routes_path}")
    nav_path = repo_root / ".github" / "site-fixes" / "js" / "ref_nav.js"

    routes_changed, routes_added = patch_v6_routes(routes_path)
    nav_changed, nav_added = patch_ref_nav(nav_path)
    return {
        "routes_changed": routes_changed,
        "routes_added": routes_added,
        "nav_exists": nav_path.exists(),
        "nav_changed": nav_changed,
        "nav_added": nav_added,
    }


def _run_node_check(js_path: Path) -> None:
    node = shutil.which("node")
    if not node:
        return
    res = subprocess.run([node, "--check", str(js_path)], capture_output=True, text=True)
    if res.returncode != 0:
        raise AssertionError(f"node --check failed on {js_path}: {res.stderr}")


def selftest() -> None:
    sample_routes = """import { ui } from "./ui.js";

const M = (file, fn, opts = {}) => ({ file, fn, ...opts });

export const ROUTES = {
  "inspections-483-recalls": M("inspections_483_recalls.js", "inspections483RecallsPage", { args: "c" }),
};

export async function v6Route(path, view) {
  const slug = path.replace(/^\\/(ref|explore)\\//, "");
  const spec = ROUTES[slug];
  if (!spec) return false;
  return true;
}
"""
    sample_nav = """export const REF_SECTIONS = [
  { title: "Science & modalities", slugs: ["drug-discovery-basics"] },
  { title: "Manufacturing & quality", slugs: ["gmp-cleanrooms"] },
  { title: "Regulatory & policy", slugs: ["fda-nda-bla"] },
  { title: "Clinical & safety", slugs: ["clinical-trials-phases"] },
];
"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "package.json").write_text('{"type": "module"}\n', encoding="utf-8")
        js_dir = root / ".github" / "site-fixes" / "js"
        js_dir.mkdir(parents=True)
        routes_file = js_dir / "v6_routes.js"
        nav_file = js_dir / "ref_nav.js"
        routes_file.write_text(sample_routes, encoding="utf-8")
        nav_file.write_text(sample_nav, encoding="utf-8")

        r1 = apply_patch(root)
        assert r1["routes_changed"] is True and len(r1["routes_added"]) == 6, r1
        assert r1["nav_changed"] is True and len(r1["nav_added"]) == 6, r1

        r2 = apply_patch(root)
        assert r2["routes_changed"] is False and r2["routes_added"] == [], r2
        assert r2["nav_changed"] is False and r2["nav_added"] == [], r2

        routes_txt = routes_file.read_text(encoding="utf-8")
        v6route_idx = routes_txt.index("export async function v6Route")
        for slug, js_file, fn_name, _ in MODULES:
            idx = routes_txt.index(f'"{slug}": M("{js_file}", "{fn_name}", {{ args: "c" }})')
            assert idx < v6route_idx, f"{slug} landed inside v6Route!"

        _run_node_check(routes_file)
        _run_node_check(nav_file)
    print("V62S_TO_V62X_ROUTE_AND_NAV_WIRING_V2_SELFTEST_PASSED")


def main() -> None:
    parser = argparse.ArgumentParser(description="Wire v6.2s-v6.2x routes into v6_routes.js and ref_nav.js")
    parser.add_argument("--apply", type=Path, help="Path to pill-by-pill repository root")
    parser.add_argument("--selftest", action="store_true", help="Run self-test with node --check")
    args = parser.parse_args()
    if args.selftest:
        selftest()
    elif args.apply:
        res = apply_patch(args.apply)
        print(res)
    else:
        parser.error("Specify --apply <repo_root> or --selftest")


if __name__ == "__main__":
    main()
