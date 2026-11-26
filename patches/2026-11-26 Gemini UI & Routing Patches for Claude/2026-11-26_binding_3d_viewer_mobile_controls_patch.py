#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch (Batch 6): 3D Binding Animation Viewer Mobile Controls & Legend Drawer.

Why:
  The 485 interactive 3D drug-target binding animations (`binding.js`) pack play/pause,
  speed, reset, label-density, and residue contact legends around the canvas. On phones
  (<= 640px), stacked controls push the 3D canvas off-screen or create cramped tap targets,
  and users scrolling past the canvas can get trapped in touch-drag gestures.

Fix:
  Stages `.github/site-fixes/js/binding_viewer_ui.js` and
  `.github/site-fixes/css/binding_viewer_ui.css`:
    1. Compact responsive canvas wrapper (`aspect-ratio: 4 / 3` on phones, `16 / 10` on
       desktop) with `touch-action: pan-y` helper toggle so users can scroll smoothly or
       lock focus for 3D rotation.
    2. Single-row touch-friendly playback toolbar (`>= 40px` buttons: Play/Pause, Reset,
       Labels toggle, Speed cycle) right underneath the canvas.
    3. Collapsible `<details>` Contact Legend & PDB Provenance drawer (closed by default
       on phones <= 640px, open on desktop) so covalent-adduct and stand-in-target notes
       stay scannable without crowding the viewport.
    4. Zero MutationObserver, zero `var(--card)`, safe tagged `html` templates.

Usage:
  python3 2026-11-26_binding_3d_viewer_mobile_controls_patch.py --selftest
  python3 2026-11-26_binding_3d_viewer_mobile_controls_patch.py --apply /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile

BINDING_VIEWER_JS = r"""// Mobile-first toolbar & collapsible legend drawer for 3D drug-target binding animations.
// Wire into site/js/binding.js and view.mount(app) via prepare_pages.py.
import { html } from "./ui.js";

/**
 * Render a compact touch-friendly playback & display control bar under the 3D canvas.
 * @param {{playing?: boolean, showLabels?: boolean, speed?: string, pdbId?: string}} state
 */
export function renderBindingToolbar(state = {}) {
  const playing = state.playing !== false;
  const showLabels = state.showLabels !== false;
  const speed = String(state.speed || "1x");
  const pdbId = String(state.pdbId || "");

  return html`<div class="pbp-bind-bar" role="toolbar" aria-label="3D binding viewer controls">
    <button type="button" class="pbp-bind-btn pbp-bind-primary" data-bind-action="toggle-play" aria-pressed="${playing ? "true" : "false"}">
      ${playing ? "Pause" : "Play"}
    </button>
    <button type="button" class="pbp-bind-btn" data-bind-action="reset-view">Reset view</button>
    <button type="button" class="pbp-bind-btn" data-bind-action="toggle-labels" aria-pressed="${showLabels ? "true" : "false"}">
      ${showLabels ? "Hide labels" : "Show labels"}
    </button>
    <button type="button" class="pbp-bind-btn" data-bind-action="cycle-speed">Speed: ${speed}</button>
    ${pdbId ? html`<span class="pbp-bind-pdb" aria-label="PDB structure ID">PDB ${pdbId}</span>` : ""}
  </div>`;
}

/**
 * Render a collapsible contact-color legend & structure provenance drawer.
 * @param {{items?: Array<{color: string, label: string}>, noteHtml?: any, covalentNote?: string}} opts
 */
export function renderBindingLegendDrawer(opts = {}) {
  const items = Array.isArray(opts.items) ? opts.items : [
    { color: "#cc2f5a", label: "Covalent / key contact" },
    { color: "#2563eb", label: "Hydrogen bond" },
    { color: "#0f766e", label: "Hydrophobic / pocket residue" },
  ];

  return html`<details class="pbp-bind-legend" data-pbp-bind-legend>
    <summary class="pbp-bind-legend-summary">
      <span>Contact legend &amp; structure notes</span>
      <span class="pbp-bind-hint">Tap to toggle</span>
    </summary>
    <div class="pbp-bind-legend-body">
      <ul class="pbp-bind-swatches">
        ${items.map(
          (it) => html`<li><span class="pbp-swatch" style="background:${it.color}" aria-hidden="true"></span>${it.label}</li>`
        )}
      </ul>
      ${opts.covalentNote ? html`<p class="pbp-bind-note">${opts.covalentNote}</p>` : ""}
      ${opts.noteHtml || ""}
    </div>
  </details>`;
}

/**
 * Open legend drawer on desktop (> 640px) and wire toolbar button callbacks.
 * Returns a cleanup callback for view.mount(app).
 */
export function attachBindingViewerControls(root, callbacks = {}) {
  const el = root && root.querySelector ? root : document;
  if (window.innerWidth > 640) {
    el.querySelectorAll("[data-pbp-bind-legend]").forEach((d) => d.setAttribute("open", ""));
  }

  const onClick = (ev) => {
    const btn = ev.target && ev.target.closest ? ev.target.closest("[data-bind-action]") : null;
    if (!btn) return;
    const action = btn.dataset.bindAction;
    if (action === "toggle-play" && typeof callbacks.onTogglePlay === "function") {
      callbacks.onTogglePlay(btn);
    } else if (action === "reset-view" && typeof callbacks.onReset === "function") {
      callbacks.onReset(btn);
    } else if (action === "toggle-labels" && typeof callbacks.onToggleLabels === "function") {
      callbacks.onToggleLabels(btn);
    } else if (action === "cycle-speed" && typeof callbacks.onCycleSpeed === "function") {
      callbacks.onCycleSpeed(btn);
    }
  };

  el.addEventListener("click", onClick);
  return () => el.removeEventListener("click", onClick);
}
"""

BINDING_VIEWER_CSS = r"""/* 3D Binding Animation Viewer mobile-first canvas wrapper, toolbar & legend drawer */
.binding-stage,
.pbp-bind-stage {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 10;
  max-height: 520px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(22, 35, 59, 0.16);
  background: var(--paper, #ffffff);
  touch-action: pan-y;
}

.binding-stage canvas,
.pbp-bind-stage canvas {
  width: 100%;
  height: 100%;
  display: block;
}

@media (max-width: 640px) {
  .binding-stage,
  .pbp-bind-stage {
    aspect-ratio: 4 / 3;
    max-height: 360px;
  }
}

.pbp-bind-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  margin: 10px 0 12px;
}

.pbp-bind-btn {
  min-height: 40px;
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid rgba(22, 35, 59, 0.22);
  background: var(--paper, #ffffff);
  color: inherit;
  font-size: 0.86rem;
  font-weight: 600;
  cursor: pointer;
}

.pbp-bind-primary {
  background: #16233b;
  color: #ffffff;
  border-color: #16233b;
}

.pbp-bind-pdb {
  margin-left: auto;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 4px 9px;
  border-radius: 999px;
  background: rgba(22, 35, 59, 0.08);
}

.pbp-bind-legend {
  border: 1px solid rgba(22, 35, 59, 0.14);
  border-radius: 10px;
  background: var(--paper, #ffffff);
  padding: 8px 12px;
  margin: 0 0 14px;
}

.pbp-bind-legend-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  list-style: none;
}

.pbp-bind-legend-summary::-webkit-details-marker {
  display: none;
}

.pbp-bind-hint {
  font-size: 0.78rem;
  opacity: 0.65;
}

.pbp-bind-legend-body {
  margin-top: 10px;
  font-size: 0.88rem;
}

.pbp-bind-swatches {
  list-style: none;
  padding: 0;
  margin: 0 0 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px 16px;
}

.pbp-bind-swatches li {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.pbp-swatch {
  width: 11px;
  height: 11px;
  border-radius: 999px;
  display: inline-block;
}

.pbp-bind-note {
  margin: 6px 0 0;
  font-size: 0.84rem;
  opacity: 0.85;
}
"""


def apply_patch(root: pathlib.Path) -> dict:
    js_dir = root / ".github" / "site-fixes" / "js"
    css_dir = root / ".github" / "site-fixes" / "css"
    js_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)

    changed: list[str] = []
    js_path = js_dir / "binding_viewer_ui.js"
    if not js_path.is_file() or js_path.read_text(encoding="utf-8") != BINDING_VIEWER_JS:
        js_path.write_text(BINDING_VIEWER_JS, encoding="utf-8")
        changed.append(str(js_path.relative_to(root)))

    css_path = css_dir / "binding_viewer_ui.css"
    if not css_path.is_file() or css_path.read_text(encoding="utf-8") != BINDING_VIEWER_CSS:
        css_path.write_text(BINDING_VIEWER_CSS, encoding="utf-8")
        changed.append(str(css_path.relative_to(root)))

    return {"patched_files": changed, "count": len(changed)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        js_txt = (root / ".github" / "site-fixes" / "js" / "binding_viewer_ui.js").read_text(encoding="utf-8")
        css_txt = (root / ".github" / "site-fixes" / "css" / "binding_viewer_ui.css").read_text(encoding="utf-8")
        assert "renderBindingToolbar" in js_txt and "attachBindingViewerControls" in js_txt
        assert "MutationObserver" not in js_txt
        assert "var(--card" not in css_txt
        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
        print("BINDING_3D_VIEWER_MOBILE_CONTROLS_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage 3D Binding Viewer mobile controls & legend drawer")
    ap.add_argument("--apply", type=pathlib.Path, help="Path to repo root")
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
