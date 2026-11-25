#!/usr/bin/env python3
"""Pill by Pill release merger & hygiene utility (v5.18+).

Safely overlays one or more *-changed-files.zip archives onto a base site zip
(e.g., v5.16 base + v5.17 changed-files + v5.18 changed-files) to produce a
clean, deploy-ready Netlify / Cloudflare Pages zip with SHA-256 verification.

Also supports --clean-source to strip __pycache__/*.pyc and OS junk from
pill-by-pill-source_v5.x.zip archives.

Usage:
  # Build a deployable v5.17 site zip from v5.16 base + v5.17 delta:
  python3 2026-11-19_merge_site_release.py \
      --base 2026-11-17_pill-by-pill-site_v5.16.zip \
      --overlay 2026-11-17_pill-by-pill-site_v5.17-changed-files.zip \
      --out 2026-11-19_pill-by-pill-site_v5.17.zip

  # Clean __pycache__ / .pyc / .DS_Store from a source archive:
  python3 2026-11-19_merge_site_release.py \
      --clean-source 2026-11-19_pill-by-pill-source_v5.18.zip \
      --out 2026-11-19_pill-by-pill-source_v5.18_clean.zip
"""
import argparse
import hashlib
import json
import pathlib
import sys
import zipfile

JUNK_PARTS = {"__pycache__", ".DS_Store", "__MACOSX"}
JUNK_SUFFIXES = (".pyc", ".pyo")
SKIP_OVERLAY_NAMES = {"README.md", "README.txt", "README"}


def is_junk(name: str) -> bool:
    p = pathlib.PurePosixPath(name)
    if any(part in JUNK_PARTS for part in p.parts):
        return True
    if p.suffix.lower() in JUNK_SUFFIXES:
        return True
    return False


def strip_common_root(names: list[str], required_marker: str | None = None) -> str:
    """Detect a single top-level directory prefix (e.g., 'site/' or 'pbp/') if all files share it."""
    files = [n for n in names if not n.endswith("/") and not is_junk(n)]
    if not files:
        return ""
    first_parts = {pathlib.PurePosixPath(f).parts[0] for f in files if len(pathlib.PurePosixPath(f).parts) > 1}
    if len(first_parts) == 1:
        root = next(iter(first_parts))
        if all(f.startswith(root + "/") for f in files):
            if required_marker is None or (root + "/" + required_marker) in files:
                return root + "/"
    return ""


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def merge_site_zips(base_path: pathlib.Path, overlay_paths: list[pathlib.Path], out_path: pathlib.Path) -> dict:
    entries: dict[str, bytes] = {}
    with zipfile.ZipFile(base_path, "r") as zf:
        root = strip_common_root(zf.namelist(), required_marker="index.html")
        for info in zf.infolist():
            if info.is_dir() or is_junk(info.filename):
                continue
            rel = info.filename[len(root):] if root and info.filename.startswith(root) else info.filename
            entries[rel] = zf.read(info.filename)

    replaced: list[str] = []
    added: list[str] = []
    skipped_readme: list[str] = []

    for ov_path in overlay_paths:
        with zipfile.ZipFile(ov_path, "r") as zf:
            ov_root = strip_common_root(zf.namelist())
            for info in zf.infolist():
                if info.is_dir() or is_junk(info.filename):
                    continue
                rel = info.filename[len(ov_root):] if ov_root and info.filename.startswith(ov_root) else info.filename
                if pathlib.PurePosixPath(rel).name in SKIP_OVERLAY_NAMES and "/" not in rel:
                    skipped_readme.append(f"{ov_path.name}:{rel}")
                    continue
                data = zf.read(info.filename)
                if rel in entries:
                    if rel not in replaced:
                        replaced.append(rel)
                else:
                    if rel not in added:
                        added.append(rel)
                entries[rel] = data

    # Sanity checks on merged site bundle
    if "index.html" not in entries:
        raise ValueError("Merged archive is missing index.html")
    version_info = None
    if "version.json" in entries:
        version_info = json.loads(entries["version.json"].decode("utf-8"))
    for key, raw in entries.items():
        if key.endswith(".json") and not key.startswith("mol/") and not key.startswith("bind/"):
            try:
                json.loads(raw.decode("utf-8"))
            except Exception as exc:
                raise ValueError(f"Invalid JSON in {key}: {exc}") from exc

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as out_zf:
        for rel in sorted(entries):
            out_zf.writestr(rel, entries[rel])

    return {
        "out": str(out_path),
        "files": len(entries),
        "bytes": out_path.stat().st_size,
        "sha256": sha256_file(out_path),
        "version": version_info,
        "replaced": sorted(replaced),
        "added": sorted(added),
        "skipped_readme": skipped_readme,
    }


def clean_source_zip(src_path: pathlib.Path, out_path: pathlib.Path) -> dict:
    kept = 0
    removed: list[str] = []
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(src_path, "r") as zin, zipfile.ZipFile(
        out_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6
    ) as zout:
        for info in zin.infolist():
            if info.is_dir():
                continue
            if is_junk(info.filename):
                removed.append(info.filename)
                continue
            zout.writestr(info.filename, zin.read(info.filename))
            kept += 1
    return {
        "out": str(out_path),
        "kept": kept,
        "removed_count": len(removed),
        "removed": sorted(removed),
        "bytes": out_path.stat().st_size,
        "sha256": sha256_file(out_path),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Merge Pill by Pill site deltas or clean source zips.")
    ap.add_argument("--base", type=pathlib.Path, help="Base site zip (e.g., v5.16)")
    ap.add_argument("--overlay", type=pathlib.Path, nargs="+", help="One or more changed-files zips to apply in order")
    ap.add_argument("--clean-source", type=pathlib.Path, help="Source zip to strip __pycache__/*.pyc and OS junk from")
    ap.add_argument("--out", type=pathlib.Path, required=True, help="Output zip path")
    args = ap.parse_args(argv)

    if args.clean_source:
        res = clean_source_zip(args.clean_source, args.out)
    elif args.base and args.overlay:
        res = merge_site_zips(args.base, args.overlay, args.out)
    else:
        ap.error("Provide either (--base and --overlay) or --clean-source")
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
